"""
对表面格点进行归类，进行最小化采样。
对采样结果进行插值，扩展。
TODO: Debug MDS plot cluster
TODO: 设置距离 cutoff，同时考虑数目 cutoff
TODO：设置某些原子（序号、类型）不进行采样，作图的时候使用最大值填充？
TODO: 根据向量的差异性计算推荐初始采样数目，可能需要测试几个不同结构试试：Ru，In2O3，Fe5C2，钙钛矿等更复杂的体系。
TODO: 向量差异性应该需要使用原生的 vector 进行计算，PCA 以后会归一化。
TODO: 双结合位点情况。表面位点采样[(x1, y1, z1), (x2, y2, z2)]。一般化双格点采样，可以找到相对应的 (COM, bondlen, theta, phi)
      不同的键长，对应不同的双格点，

TODO: 构效关系建立。将不同的位点向量合并，然后进行性能分布的关联，投影到二维平面（PCA）。
"""

import pickle
from logging import warning

import matplotlib.tri as mtri
import numpy as np
from ase.data import covalent_radii, vdw_radii
from ase.geometry import find_mic
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
from scipy.spatial import ConvexHull
from scipy.spatial.distance import euclidean, cdist
from sklearn.cluster import KMeans as Cluster
from sklearn.decomposition import PCA
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.preprocessing import StandardScaler

from surface_construct.sampling import InitialSampling, addition_samples
from surface_construct.utils import get_calc_info, GridGenerator, get_distances, furthest_sites


def no_weight(v, **kwargs):
    return v


def linear_weight(v, **kwargs):
    r0 = kwargs['r0']
    if 'rc' in kwargs:
        rc = kwargs['rc']
    else:
        rc = 3 * r0

    w = (rc - v) / (rc - r0)
    w[w > 1.0] = 1.0
    w[w < 0.0] = 0.0
    v_w = w
    return v_w


def vb_r_weight(v, **kwargs):
    r0 = kwargs['r0']
    if 'b' not in kwargs:
        b = 0.618 # 较大的数值衰减较慢，能够将更远的原子作用考虑进来。不建议大于此数
    else:
        b = kwargs['b']
    weight = np.exp((r0 - v) / b)
    weight[weight > 1.0] = 1.0
    v_w = v / r0 * weight
    return v_w


def vb_weight(v, **kwargs):
    r0 = kwargs['r0']
    if 'b' not in kwargs:
        b = 1.0  # 较大的数值衰减较慢，能够将更远的原子作用考虑进来
    else:
        b = kwargs['b']
    weight = np.exp((r0 - v) / b)
    weight[weight > 1.0] = 1.0
    v_w = weight
    return v_w


def reciprocal_weight(v, **kwargs):
    """Relate to Coulumb interaction
    Need charge for each atom.
    TODO: add charge option.
    Calculate each pairs between q and q_ads.
    q = kwargs.get('charge',0.1)
    q_ads = kwargs.get('charge_ads',1)
    q 可以使用 CHELG 方法快速计算。
    """
    r0 = kwargs['r0']
    v_w = r0 / v
    return v_w

# TODO: vdw 相互作用项

# TODO: 总的加和是 valent + coulumb + vdw，或者三者的合并

def reciprocal_square_weight(v, **kwargs):
    return reciprocal_weight(v, **kwargs) ** 2


class SurfaceGrid:

    def __init__(self, atoms, interval=None, vlen=10,
                 ads_num=6,
                 rads=None,
                 radii=None,
                 radii_type='covalent_radii',
                 radii_factor=1.0,
                 lpca=True,
                 cutoff=10,
                 ):
        self.atoms = atoms
        num_set = set(self.atoms.numbers)
        num_list = list(self.atoms.numbers)
        self.species = sorted([(num, num_list.count(num)) for num in num_set], key=lambda x: x[0])
        if interval is None:
            interval = 0.1  # 默认格点间距 0.1 A

        if radii is None:
            if radii_type == 'covalent_radii':
                radii = covalent_radii * radii_factor
            elif radii_type == 'vdw_radii':
                radii = vdw_radii * radii_factor
            else:
                raise NotImplementedError
        self.radii = radii
        self.cutoff = cutoff
        if rads is not None:
            self.rads = rads
        else:
            self.rads = self.radii[ads_num]

        self.interval = interval
        self.vlen = vlen

        self.points = None  # 格点 xyz 坐标
        self._Dga = None  # grid_atoms 距离矩阵
        # self._DAga = None  # grid_atoms 距离向量矩阵，保存是为了求角度
        self.vector = None
        self.lpca = lpca
        self._pca = None
        self._raw_vector = None
        self._reduced_vector = None
        self._vector_dim = None

        self._sample_vector = []  # 用于作图 和 GPR
        self._clusters = None  # 仅用于作图

        nx = int(self.atoms.cell.cellpar()[0] / self.interval)  # 间隔是格点的五分之一
        ny = int(self.atoms.cell.cellpar()[1] / self.interval)  # 间隔是格点的五分之一
        self.grid_nx = nx
        self.grid_ny = ny

        # self.grid_energy, self.grid_energy_sigma = None, None
        # self.sample_energy = None
        self.sample_idx = None  # 采样点的 idx
        self.sample_points = None

        self.sample_property = {}
        self.grid_property = {}
        self.grid_property_sigma = {}

        self.calc_info = {}
        if atoms.calc is not None:
            self.calc_info = get_calc_info(atoms.calc)

        self.iter = 0  # 记录进行了多少次的迭代

    def initialize(self):
        # 格点化
        self.gridize()
        # 格点向量化
        self.vectorize(pca=self.lpca)

    def structure_boundary(self):
        result = np.zeros((3, 2))  # [[xmin, xmax], [ymin, ymax], [zmin, zmax]]
        for dim in (0, 1, 2):
            for func, sign in zip((np.argmin, np.argmax), (-1, 1)):
                atom_idx = func(self.atoms.positions[:, dim])
                v = self.atoms.positions[atom_idx, dim] + sign * (self.radii[self.atoms.numbers[atom_idx]] + self.rads)
                result[dim, int((sign+1)/2)] = v
        return np.concatenate(result)  # [xmin, xmax, ymin, ymax, zmin, zmax]

    def gridize(self, **kwargs):
        """
        格点化。
        这种方法仅仅适用于无孔的材料，表面为z方向，且方向向上。
        * gridxy: [X, Y] 2D meshgrid
        * surface_index: 表面原子的序号
        :return:
        """
        subtype = kwargs.get('subtype', 'slab')  # default is slab
        self._subtype = subtype
        rsub = [self.radii[atomnum] for atomnum in self.atoms.numbers]
        gridgen = GridGenerator(self.atoms, interval=self.interval, subtype=subtype, rads=self.rads, rsub=rsub)
        self.points = gridgen.grid
        self._gridgen = gridgen

        #self._Dga = grid_dist
        #self._DAga = grid_dist_array

    def _calc_Dga(self):
        if self.points is None:
            self.gridize()
        if self._subtype == 'slab':
            pbc = [True, True, False]
        elif self._subtype == 'cluster':
            pbc = [False, False, False]
        else:
            pbc = self.atoms.pbc
        _, Dga = get_distances(self.points, self.atoms.positions, cutoff=self.cutoff, pbc=pbc,
                               use_ase=False, cell=self.atoms.cell)
        self._Dga = Dga


    def grid_NN_array(self, grid_idx):
        """
        返回表面格点最近邻原子和次紧邻原子的向量，以此方式求格点的 reference 向量。效果比较好。
        :param grid_idx:
        :return:
        """

        if self._Dga is None:
            self._calc_Dga()
        order = np.argsort(self._Dga[grid_idx])
        p1, p2 = self.atoms.positions[order[0:2]]
        v, _ = find_mic(p2-p1, cell=self.atoms.cell, pbc=self.atoms.pbc)
        return v

    def view_grid(self):
        if self._gridgen is None:
            self.gridize()
        self._gridgen.view()

    @property
    def grid_energy(self):
        if 'energy' in self.grid_property:
            return self.grid_property['energy']
        else:
            return None

    def vectorize(self, Dga=None, return_vector=False, wf=vb_weight, pca=True, pca_ratio=0.90, **kwargs):
        """
        TODO: 使用 DScribe 来进行向量化，并进行测试。如何测试？测试什么内容？
        TODO: 产生 cluster_mesh, 生成 cluster_mesh_id 与 point_id 之间的正反向 dict
        使用 distance matrix 来进行向量化
        使用衰减函数对 vector 加权重。备选函数：S型，指数型（键价），1/sqrt，1/x，线性。倾向使用指数型，键价理论支持。 1/x，或者 1/sqrt，衰减更慢。
        这种方法类似于多点地位方法（Multilateration），因而暂时称其为 Multilateration vectorization.
        :param pca_ratio:
        :param pca:
        :param wf:
        :param Dga: grid-atoms distance matrix
        :param return_vector: 是否返回 vector 向量
        """
        if Dga is None:
            if self._Dga is None:
                self._calc_Dga()
            Dga = self._Dga

        Natoms = Dga.shape[1] / len(self.atoms)  # Dga is multiple of atoms
        assert Natoms == int(Natoms)  # Natoms should be int
        numbers = np.concatenate([self.atoms.numbers]*int(Natoms))  # multiply atoms.number

        vector = []
        for atomnum, atomcount in self.species:
            grid_dist = Dga[:, numbers == atomnum]
            # 排序，返回排序后的序号
            index_array = grid_dist.argsort(axis=-1)
            grid_dist = np.take_along_axis(grid_dist, index_array, axis=-1)
            # grid_dist_array = np.take_along_axis(grid_dist_array, index_array, axis=-1)
            # 设定距离向量长度
            vlen = self.vlen
            r0 = self.rads + self.radii[atomnum]
            v = grid_dist[:, :vlen]
            kwargs.update({'r0': r0})
            # v_w = np.concatenate([wf(v, **kwargs), np.zeros((v.shape[0], self.vlen-vlen))], axis=1)
            v_w = wf(v, **kwargs)
            vector.append(v_w)
        vector = np.concatenate(vector, axis=1)
        self._raw_vector = vector
        if not pca:  # 用于 debug
            self._vector_dim = vector.shape[1]
            if return_vector:
                return vector
            else:
                self.vector = vector
                return
        # PCA 降维
        if return_vector:
            assert self._pca is not None
            reduced_vector = self._pca.transform(vector)
            return reduced_vector
        else:
            dim_max = int(3 * len(self.species))
            pca = PCA(n_components=dim_max, whiten=False)
            pca.fit(vector)
            dim = 2
            for i in range(2, dim_max):  # 最小维度为 2
                explained_variance_ratio = sum(pca.explained_variance_ratio_[:i])
                if explained_variance_ratio > pca_ratio:
                    dim = i
                    break
            self._pca = PCA(n_components=dim, whiten=False)
            self._pca.fit(vector)
            reduced_vector = self._pca.transform(vector)
            self.vector = reduced_vector
            self._vector_dim = self.vector.shape[1]

    @property
    def _vector_unit(self):
        """
        计算实空间和向量空间的距离转化系数。随机取十个点，求平均值。
        :return:
        """
        nsample = 100
        rng = np.random.default_rng()
        idx_0 = rng.choice(range(len(self.points)-1), size=nsample)
        idx_1 = idx_0+1
        idx = np.asarray([[i,j] for i,j in zip(idx_0, idx_1) if (i not in idx_1 and j not in idx_0)])
        d_grid = np.linalg.norm(self.points[idx[:, 0]] - self.points[idx[:, 1]], axis=1)
        idx = idx[d_grid<1.2 * self.interval]
        d_vector = np.linalg.norm(self.vector[idx[:,0]]-self.vector[idx[:,1]], axis=1).mean()
        k = d_vector / self.interval
        return np.min(k)

    def grid_sample(self, N=1, probability=None, **kwargs):
        """
        Warning: Obsoleted, replaced by Sampling class
        :param probability:
        :param N:
        :return:
        """
        if 'energy' in self.grid_property:
            points_idx = addition_samples(self, size=N, probability=probability, **kwargs)
        else:
            points_idx = InitialSampling(self).samples(size=N)
        return points_idx

    # TODO: 将中心重新映射回到Cartesian坐标 ：
        # 找到向量空间最紧邻的N个点，判断其实空间的距离是否小于 interval × 2，直到有三个点满足
        # 然后进行空间变换 A x M = B，M = B / A = B x A-1, R = V x M
        # 或者直接使用最近邻点的坐标

    def plot_cluster(self, figname=None):
        """
        :param figname:
        :return:
        """
        if figname is None:
            figname = 'site_cluster.png'
        print("Plot the site verctor and cluster ...")
        if self._pca:
            reduced_vector = self._mesh_centers[:,:2]
            sample_vector = self._sample_vector
        else:
            pca = PCA(n_components=2)
            pca.fit(self.vector)
            reduced_vector = pca.transform(self._mesh_centers)
            sample_vector = pca.transform(self._sample_vector)
        # Obtain labels for each point
        # plot in vector space
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.scatter(reduced_vector[:, 0], reduced_vector[:, 1], c=self._clusters.labels_, cmap=plt.cm.Paired)
        ax.scatter(sample_vector[:, 0],sample_vector[:, 1], marker="+", s=100, linewidths=2,
                   color="black", zorder=10)
        title = f"The site vector colored in {self._clusters.n_clusters} clusters"
        ax.set_title(title)
        fig.set_dpi(300)
        fig.set_size_inches(10, 10)
        figname1 = 'vector_' + figname
        fig.savefig(figname1, bbox_inches='tight')
        plt.cla()
        plt.close("all")

        # plot grid
        labels = self._clusters.predict(self.vector)
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.scatter(self.points[:, 0], self.points[:, 1], c=labels, s=1, cmap=plt.cm.Paired)
        ax.scatter(self.sample_points[:, 0],self.sample_points[:, 1], marker="+", s=100, linewidths=2,
                   color="black", zorder=10)
        title = f"The site grid colored in {self._clusters.n_clusters} clusters"
        ax.set_title(title)
        fig.set_dpi(300)
        fig.set_size_inches(10, 10)
        figname2 = 'grid_' + figname
        fig.savefig(figname2, bbox_inches='tight')
        plt.cla()
        plt.close("all")


    def set_sample(self, sample_points, keep_old_sample=True):
        """
        手动设置采样格点，计算 self._sample_vector。z 坐标自动被忽略。
        :param keep_old_sample: 判断是否保留原有的采样的点
        :param sample_points:
        :return:
        """
        # 找到 points 对应的 z
        z = griddata(self.points[:, :2], self.points[:, 2], sample_points[:, :2])
        new_sample_points = sample_points.copy()
        new_sample_points[:, 2] = z
        # 计算 vector
        if self._subtype == 'slab':
            pbc = [True, True, False]
        elif self._subtype == 'cluster':
            pbc = [False, False, False]
        else:
            pbc = self.atoms.pbc
        DAga, Dga = get_distances(new_sample_points, self.atoms.positions,
                                  cutoff=self.cutoff,
                                  cell=self.atoms.cell, pbc=pbc)
        # 计算 points 的 vector
        vector = self.vectorize(Dga=Dga, pca=self.lpca)
        if keep_old_sample and self.sample_points is not None:
            # 要判断 sample_property 的长度，来决定sample放到哪里
            if 'energy' in self.sample_property:
                len_value = len(self.sample_property['energy'])
            else:
                len_value = 0
            self.sample_points = np.concatenate([
                self.sample_points[:len_value],
                new_sample_points,
                self.sample_points[len_value:]
            ])
            self.sample_idx = np.concatenate([
                self.sample_idx[:len_value],
                [-1] * len(new_sample_points),  # 为新的插点赋值index -1, 作为区分
                self.sample_idx[len_value:]
            ])
            self._sample_vector = np.concatenate([
                self._sample_vector[:len_value],
                vector,
                self._sample_vector[len_value:]
            ])
        else:
            self.sample_points = new_sample_points
            self.sample_idx = np.array([-1] * len(new_sample_points))
            self._sample_vector = vector
            # 重置结果
            self.sample_property = {}

    def set_property(self, values, key='energy'):
        """
        预测性质只能在能量之后，而且不支持迭代
        :param key:
        :param values:
        :return:
        """
        if key in self.sample_property:
            if len(self.sample_property[key]) == len(self._sample_vector):
                # 如果 _sample_vector 的长度与结果的长度相同，说明已经进行过回归，不需要再进行
                print("Warning: sample_vector 的长度与结果的长度相同，说明已经进行过回归，不需要再进行回归！")
                return None
            self.sample_property[key] = np.concatenate([self.sample_property[key], np.asarray(values)])
            if key == 'energy':
                self.iter += 1
        else:
            self.sample_property[key] = np.asarray(values)

        assert len(self._sample_vector) == len(self.sample_property[key])  # 这里需要保证采样的点来自于自主采样

        # Standardization of y
        scaler = StandardScaler()
        y = np.atleast_2d(self.sample_property[key]).T
        scaler.fit(y)
        y_scaled = scaler.transform(y).T[0]
        # RBF Kernel
        length_scale_grid = 1.0  # 实空间的length scale, 1 angstrom
        length_scale_vector = length_scale_grid * self._vector_unit
        length_scale_bounds = (length_scale_vector/2.0, length_scale_vector*2.0)
        # length_scale_bounds = 'fixed'
        # length_scale = [length_scale_vector] * self._vector_dim  # 向量空间的 length_scale, anisotropic
        length_scale = length_scale_vector  # 向量空间的 length_scale, isotropic
        rbf_kernel = RBF(length_scale=length_scale, length_scale_bounds=length_scale_bounds)
        # noise kernel
        noise_level_dict = {
            'energy': 0.01,  # eV
            'phi': 0.05,  # angle
        }
        if key in noise_level_dict:
            noise_level = noise_level_dict[key]  # eV
        else:
            noise_level = 0.001
        noise_level_norm = np.abs(noise_level / scaler.scale_[0])  # 标准化缩放
        white_kernel = WhiteKernel(noise_level=noise_level_norm, noise_level_bounds='fixed')
        # 总的 kernel
        constant_kernel = ConstantKernel(constant_value=1.0, constant_value_bounds='fixed')
        kernel = constant_kernel * rbf_kernel + white_kernel
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, alpha=noise_level_norm*0.01)
        print(f"Kernel parameters before fit:{kernel})")
        gp.fit(self._sample_vector, y_scaled)
        # 打印 GPR 结果
        print(f"Kernel parameters after fit: {gp.kernel_} \n"
              f"Log-likelihood: {gp.log_marginal_likelihood(gp.kernel_.theta):.3f}")
        # 为 self.points 插值
        y_predict_scaled, y_sigma_predict_scaled = gp.predict(self.vector, return_std=True)
        # 逆向求真实数值
        y_predict_scaled = np.atleast_2d(y_predict_scaled).T
        self.grid_property[key] = scaler.inverse_transform(y_predict_scaled).T[0]
        self.grid_property_sigma[key] = y_sigma_predict_scaled * np.abs(scaler.scale_[0])  # 误差不需要逆向求值，只需要系数

    def plot_property(self, key='energy', sample=True, figname=None, vmax=None, vmin=None):
        """
        TODO: 支持 cluster 作图。保存原始 meshgrid 和 id？或者重新插值？
        :param key: 画图的内容，对应于 grid_property 中的 key
        :param sample: 是否画上 sample 点，默认是
        :param figname: 图片名字，默认 key_iter_niter.png
        :param vmax: colorbar 最大值，默认自动
        :param vmin: colorbar 最小值，默认自动
        :return:
        """
        assert key in self.grid_property
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        print(f"Plot {key} ...")
        x = self.points[:, 0]
        y = self.points[:, 1]
        z = self.grid_property[key]
        triang = mtri.Triangulation(x, y)
        contourf0 = ax.tricontourf(triang, z, levels=50, cmap="jet", vmin=vmin, vmax=vmax)

        # 画上 sample 点，采过的点用黑色，下一步采的点用白色
        if sample:
            sample_points = self.sample_points
            nsampled = len(self.sample_property['energy'])
            ax.scatter(sample_points[0:nsampled, 0], sample_points[0:nsampled, 1], marker="+", s=100, linewidths=2,
                       color="black", zorder=10)
            ax.scatter(sample_points[nsampled:, 0], sample_points[nsampled:, 1], marker="o", s=100, linewidths=2,
                       color="w", zorder=10)
        fig.colorbar(contourf0, ax=ax)
        title = f"{key.capitalize()} distribution, Max(sigma)={self.grid_property_sigma[key].max():.3f}"
        ax.set_title(title)
        fig.set_dpi(300)
        fig.set_size_inches(10, 10)
        if figname is None:
            figname = key + '_iter' + str(self.iter) + '.png'
        fig.savefig(figname, bbox_inches='tight')

        plt.cla()
        plt.close("all")

    def set_energy(self, values):
        """
        TODO: 保留了以前的运行命令，但是其他参数都不起作用了
        TODO: 新的模块需要测试
        :param values:
        :return:
        """
        self.set_property(values)

    def plot_energy(self, figname=None, vmax=None, vmin=None):
        """
        TODO: 保留了以前的运行命令，但是其他参数都不起作用了
        TODO: 新的模块需要测试
        :param figname:
        :param vmax:
        :param vmin:
        :return:
        """
        self.plot_property(figname=figname, vmax=vmax, vmin=vmin)

    def line_profile(self, path=None, key='energy'):
        """
        画出给定路径的能量扫面曲线图
        :param path:
        :param key:
        :return:
        """
        if key not in self.grid_property:
            raise KeyError
        if len(path) < 2:
            raise ValueError
        # 路径格点
        line_points = None
        path_length = 0.0
        for i in range(1, len(path[1:])+1):
            length = euclidean(path[i], path[i-1])
            path_length += length
            n = int(length / self.interval) + 1
            x = np.linspace(path[i-1][0], path[i][0], n, endpoint=False)
            y = np.linspace(path[i-1][1], path[i][1], n, endpoint=False)
            if line_points is not None:
                line_points = np.concatenate([line_points, np.array([x, y]).T])
            else:
                line_points = np.array([x, y]).T
        line_points = np.concatenate([line_points, [path[-1]]])
        # 插值
        line_values = griddata(points=self.points[:, 0:2],
                               values=self.grid_property[key],
                               xi=line_points,
                               method='linear')

        line_x = np.linspace(0.0, path_length, len(line_values))
        return line_x, line_values

    def plot_sigma(self, key='energy', figname=None, vmax=None, vmin=None):
        # TODO: 支持 cluster 作图。保存原始 meshgrid 和 id？或者重新插值？
        assert key in self.grid_property_sigma
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        x = self.points[:, 0]
        y = self.points[:, 1]
        z = self.grid_property_sigma[key]
        triang = mtri.Triangulation(x, y)
        contourf0 = ax.tricontourf(triang, z, levels=50, cmap="RdPu", vmin=vmin, vmax=vmax)

        # sigma 最大值标注
        max_sigma_point = self.points[self.grid_property_sigma[key].argmax()]
        ax.scatter(max_sigma_point[0], max_sigma_point[1], marker="+", s=100, linewidths=2,
                   color="w", zorder=10)
        fig.colorbar(contourf0, ax=ax)
        title = f"Gaussian Process Error of {key.capitalize()}, Max(sigma)={self.grid_property_sigma[key].max():.3f} eV"
        ax.set_title(title)

        fig.set_dpi(300)
        fig.set_size_inches(10, 10)
        if figname is None:
            figname = key + '_sigma_iter' + str(self.iter) + '.png'
        fig.savefig(figname, bbox_inches='tight')
        plt.cla()
        plt.close("all")

    def error(self):
        """
        TODO: 改为 @property，默认返回无穷大
        TODO: 假设点越多，误差越小。计算倒数第二帧与最后一帧之间的平均误差或者方差
        TODO：输出前面不同帧的误差变化曲线
        :return:
        """
        if 'energy' in self.grid_property_sigma:
            return self.grid_property_sigma['energy'].max()
        else:
            print("No energy for points!")
            return None

    def to_pkl(self, pkl_file="surface_grid.pkl"):
        file_pi = open(pkl_file, 'wb')
        pickle.dump(self, file_pi)
        file_pi.close()

    @classmethod
    def from_pkl(cls, pkl_file="surface_grid.pkl"):
        filehandler = open(pkl_file, 'rb')
        obj = pickle.load(filehandler)
        filehandler.close()
        return obj


def combine_sg_vector(*sg_lst):
    """
    TODO: 使用 class 对多个 sg 进行管理，合并等等
    合并 sg.vector to a larger vector set, in order to plot it
    :param sg_lst:
    :return:
    """

    if len(sg_lst) == 0:
        return None
    elif len(sg_lst) == 1:
        return sg_lst[0]._raw_vector

    species_num_lst = sorted(set([s[0] for sg in sg_lst for s in sg.species]))
    species_default_dct = {num: 0 for num in species_num_lst}
    species_lsts = []
    vlen_max = species_default_dct.copy()
    for sg in sg_lst:
        species_dct = species_default_dct.copy()
        species_dct.update({num: min(sg.vlen, cnt) for num, cnt in sg.species})
        # 对 species_dcts 中的元素进行排序
        species_lst = sorted(species_dct.items(), key=lambda x: x[0])
        species_lsts.append(species_lst)
        vlen_max = {num: max(vlen_max[num], vlen) for num, vlen in species_dct.items()}  # 更新向量最大值
    # 对 vlen_max 进行排序

    new_vector_lst = []
    for sg, species_lst in zip(sg_lst, species_lsts):
        # 提取 raw_vector, 对不足的 vector 进行补齐
        raw_vector = sg._raw_vector
        nvector = len(raw_vector)  # 总行数
        pointer = 0  # 列指针
        new_vector = []
        for num, cnt in species_lst:
            new_vlen = vlen_max[num]
            new_v = np.zeros([nvector, new_vlen])
            new_v += 1.0 * raw_vector.min()  # 超过截断的使用最小值的三分之二，从而减小不同表面之间的结构差异
            # 判断长度是不是 0
            if cnt == 0:
                new_vector.append(new_v)
                continue
            # 取出对应的 vector 列
            old_v = raw_vector[:, pointer:pointer+cnt]
            # 判断是不是要补齐
            if cnt == new_vlen:
                new_vector.append(old_v)
            else:
                new_v[:, :cnt] = old_v
                new_vector.append(new_v)
            pointer += cnt
        new_vector = np.concatenate(new_vector, axis=1)
        new_vector_lst.append(new_vector)
    vector_combine = np.concatenate(new_vector_lst, axis=0)

    return vector_combine
