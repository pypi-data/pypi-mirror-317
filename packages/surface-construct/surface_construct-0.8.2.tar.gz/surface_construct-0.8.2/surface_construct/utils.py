import itertools

import ase
import ase.geometry
import numpy as np
from ase.data import vdw_radii, chemical_symbols
from ase.neighborlist import natural_cutoffs
from ase.visualize import view
from scipy.sparse import coo_matrix
from scipy.spatial import ConvexHull, cKDTree
from skimage.measure import marching_cubes


def calc_hull_vertices(v):
    shape = v.shape
    if len(shape) != 2:
        print(f"Warning: The vector should be 2D, however {len(shape)}D vector was provided!)")
        print("The Convex Hull Vertices won't be calculated.")
        return None
    if shape[1] > 5:
        print(f"Warning: The vector.shape[1]={shape[1]} is too large to be calculated!)")
        print("The Convex Hull Vertices won't be calculated.")
        return None
    try:
        print("Calculate Convex Hull Vertices ...")
        hull = ConvexHull(v)
        vertices = hull.vertices
        return vertices
    except ValueError:
        return None


def get_calc_info(calc=None):
    if calc is None:
        return {}
    calc_name = calc.name
    calc_para = dict()
    if calc_name in ('vasp',):
        calc_para['xc'] = calc.parameters['xc']
        calc_para['encut'] = calc.parameters['encut']

    calc_info = {
        'name': calc_name,
        'para': calc_para,
    }
    return calc_info


def get_distances(p1, p2=None, cutoff=10, cell=None, pbc=None, use_ase=False):
    """
    计算位点周围原子的距离，参考 ase.geometry.get_distances. 对于更大的体系使用 cDTree 来计算。
    :param pbc:
    :param p1: grid positions
    :param p2: atoms.positions
    :param cutoff: 截断半径，只考虑距离之内的距离，超过该距离的定为 np.inf
    :param cell:
    :param use_ase: 如果 use_ase is True，则使用 ase.geometry.get_distances，即周期性条件等价的原子只考虑一次
    :return:
    """
    ncell = np.floor((cutoff * 2) / cell.lengths())
    for ip,p in enumerate(pbc):
        if not p:  # 如果不是周期性的，则不要重复
            ncell[ip] = 0
    if np.all(ncell==1):
        use_ase = True

    if use_ase:
        return ase.geometry.get_distances(p1, p2, cell, pbc)

    if p2 is None:
        p2 = p1.copy()

    ranges = [np.arange(-1 * p, p + 1) for p in ncell]
    hkls = np.array(list(itertools.product(*ranges)))
    hkls = np.concatenate([hkls, np.zeros([hkls.shape[0], 3-hkls.shape[1]], dtype=int)], axis=1)
    vrvecs = hkls @ cell
    p2 = np.concatenate(p2 + vrvecs[:, None], axis=0)
    tree1 = cKDTree(p1, copy_data=True)
    tree2 = cKDTree(p2, copy_data=True)
    sdm = tree1.sparse_distance_matrix(tree2, max_distance=cutoff)
    dist = sdm.toarray()
    # set distance larger than cutoff to np.inf
    mask = dist==0
    dist[mask] = np.inf
    return None, dist


def iso_surface(grids, dist_array, level=0):
    verts, faces, normals, values = marching_cubes(dist_array, level=level, allow_degenerate=False)
    grid_x, grid_y, grid_z = grids
    verts = np.asarray(verts, dtype=int)
    unique_verts = np.unique(verts, axis=0)  # exclude some repeat points
    points = np.asarray([grid_x[unique_verts[:, 0], unique_verts[:, 1], unique_verts[:, 2]],
                         grid_y[unique_verts[:, 0], unique_verts[:, 1], unique_verts[:, 2]],
                         grid_z[unique_verts[:, 0], unique_verts[:, 1], unique_verts[:, 2]]]).T

    return points


class GridGenerator:
    def __init__(self, atoms,
                 rads=0.76,
                 rsub='natural_cutoff',
                 subtype=None,
                 interval=0.1,
                 scale=None,
                 ):
        """
        :param atoms: 基底结构 ase.Atoms
        :param rads: 吸附原子的半径, 默认是 C 的共价半径
        :param rsub: 基底的原子半径
            type: str, 'covalent_radii' or 'vdw_radii'
            type: list or tuple or numpy.array, [r1, r2, ... rN], N=len(atoms)
        :param subtype: 基底的类型，slab, cluster, bulk (porous material)
        :param interval:
        :param scale: scale factor of rsub and rads. For covalent_radii, the default is 1.1, otherwise it is 1.0
        """
        self.atoms = atoms
        self._grid = None
        self.atoms_num_type = sorted(set(atoms.numbers))
        self.interval = interval

        if subtype is None:
            npbc = sum(atoms.pbc)
            if npbc == 0:
                self.subtype = 'cluster'
            elif npbc == 2:
                if atoms.pbc[-1]:
                    raise "Error: Slab should be in xy direction!"
                self.subtype = 'slab'
            elif npbc == 3:
                self.subtype = 'bulk'
            else:
                raise NotImplementedError("Subtype not implemented yet!")

        elif subtype.lower() in ['slab', 'bulk', 'cluster']:
            self.subtype = subtype.lower()
        else:
            raise NotImplementedError('Only slab, cluster, bulk and slab are implemented.')
        self._generator = getattr(self, self.subtype+'_grid')

        if type(rsub) in (list, tuple, np.ndarray):
            assert len(rsub) == len(atoms)
            self.rsub = rsub
        elif type(rsub) == dict:
            self.rsub = [rsub.get(n) or rsub.get(chemical_symbols(n)) for n in atoms.numbers]
        elif type(rsub) == str:
            if rsub == 'covalent_radii' or rsub == 'natural_cutoff':
                self.rsub = natural_cutoffs(atoms)
                if scale is None:
                    scale = 1.1
            elif rsub == 'vdw_radii':
                self.rsub = [vdw_radii[n] for n in atoms.numbers]
        else:
            raise ValueError("rsub must be 'covalent_radii', 'natural_cutoff' or 'vdw_radii' or a list.")

        if scale is None:
            scale = 1.0
        self.scale = scale
        self.rsub = np.asarray(self.rsub) * scale
        self.rads = rads * scale

    def cluster_grid(self):
        atoms = self.atoms
        if np.all(atoms.pbc):
            atoms.center()
        interval = self.interval
        pos = atoms.positions
        # 找到团簇格点的边界
        posx, posy, posz = pos[:,0], pos[:,1], pos[:,2]
        xmin = (posx - self.rsub).min() - interval * 2 - self.rads
        xmax = (posx + self.rsub).max() + interval * 2 + self.rads
        ymin = (posy - self.rsub).min() - interval * 2 - self.rads
        ymax = (posy + self.rsub).max() + interval * 2 + self.rads
        zmin = (posz - self.rsub).min() - interval * 2 - self.rads
        zmax = (posz + self.rsub).max() + interval * 2 + self.rads
        xarray = np.arange(xmin, xmax, interval)
        yarray = np.arange(ymin, ymax, interval)
        zarray = np.arange(zmin, zmax, interval)
        nx,ny,nz = map(len, [xarray, yarray, zarray])
        # 格点生成
        grid_x, grid_y, grid_z = np.meshgrid(xarray, yarray, zarray, indexing='ij')
        xyz = np.asarray([grid_x.ravel(), grid_y.ravel(), grid_z.ravel()]).T
        xyz = rattle(xyz, stdev=self.interval/3)
        grid_tree = cKDTree(xyz, copy_data=True)

        dist_max = coo_matrix((1,nx*ny*nz))
        atoms_num_type = set(atoms.numbers)
        # 对于不同的原子类型取不同的半径
        for num_type in atoms_num_type:
            pos = atoms.positions[atoms.numbers == num_type]
            atoms_tree = cKDTree(pos, copy_data=True)
            max_distance = self.rads + self.rsub[atoms.numbers == num_type][0]
            sdm = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=max_distance)
            # 保证没有格点的坐标跟grid 完全重合，如果有的话，需要标识出来，赋予它们另外的值，保证在后面识别中不为0。
            sdm0 = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=0)
            for k in sdm0.keys():
                sdm[k] = 1
            dist_max = sdm.tocoo().nanmax(axis=0).maximum(dist_max)
        dist_max = dist_max.transpose().toarray().reshape((nx, ny, nz))
        points = iso_surface([grid_x, grid_y, grid_z], dist_array=dist_max, level=0)
        self._grid = points

    def slab_grid(self):
        atoms = self.atoms
        pos = atoms.positions
        interval = self.interval
        posz = pos[:,2]
        zmax = (posz + np.asarray(self.rsub)).max() + self.rads + interval * 2
        zmin = (posz.max() + posz.min())/2  # 从层中心开始
        lenx, leny, lenz = atoms.cell.lengths()
        ifx, ify, ifz = interval / lenx, interval / leny, interval / lenz
        fx_list = np.arange(0, 1, ifx)
        fy_list = np.arange(0, 1, ify)
        fz_list = np.arange(zmin/lenz, zmax/lenz, ifz)
        nx, ny, nz = map(len, [fx_list, fy_list, fz_list])
        fgrid_x, fgrid_y, fgrid_z = np.meshgrid(fx_list, fy_list, fz_list, indexing='ij')
        fxyz = np.asarray([fgrid_x.ravel(), fgrid_y.ravel(), fgrid_z.ravel()]).T
        xyz = rattle(atoms.cell.cartesian_positions(fxyz), stdev=self.interval/3)
        grid_tree = cKDTree(xyz, copy_data=True)

        # 对atoms 在 xy 方向超胞. Adapt from ase.geometry.geometry.general_find_mic
        ranges = [np.arange(-1 * p, p + 1) for p in atoms.pbc[:2]]
        hkls = np.concatenate([np.array(list(itertools.product(*ranges))),
                               np.zeros([9, 1], dtype=int)], axis=1)
        vrvecs = hkls @ atoms.cell
        super_pos = np.concatenate(atoms.positions + vrvecs[:,None], axis=0)
        super_num = np.concatenate([atoms.numbers] * 9)
        rsub = np.concatenate([self.rsub] * 9)

        dist_max = coo_matrix((1,nx*ny*nz))
        atoms_num_type = set(atoms.numbers)
        # 对于不同的原子类型取不同的半径
        for num_type in atoms_num_type:
            pos = super_pos[super_num == num_type]
            atoms_tree = cKDTree(pos, copy_data=True)
            max_distance = self.rads + rsub[super_num == num_type][0]
            sdm = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=max_distance)
            # 保证没有格点的坐标跟grid 完全重合，如果有的话，需要标识出来，赋予它们另外的值，保证在后面识别中不为0。
            sdm0 = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=0)
            for k in sdm0.keys():
                sdm[k] = 1
            dist_max = sdm.tocoo().nanmax(axis=0).maximum(dist_max)
        dist_max = dist_max.transpose().toarray().reshape((nx, ny, nz))
        fpoints = iso_surface([fgrid_x, fgrid_y, fgrid_z], dist_array=dist_max, level=0)
        points = atoms.cell.cartesian_positions(fpoints)
        self._grid = points

    def bulk_grid(self):
        atoms = self.atoms
        pos = atoms.positions
        interval = self.interval
        lenx, leny, lenz = atoms.cell.lengths()
        ifx, ify, ifz = interval / lenx, interval / leny, interval / lenz
        fx_list = np.arange(0, 1, ifx)
        fy_list = np.arange(0, 1, ify)
        fz_list = np.arange(0, 1, ifz)
        nx, ny, nz = map(len, [fx_list, fy_list, fz_list])
        fgrid_x, fgrid_y, fgrid_z = np.meshgrid(fx_list, fy_list, fz_list, indexing='ij')
        fxyz = np.asarray([fgrid_x.ravel(), fgrid_y.ravel(), fgrid_z.ravel()]).T
        xyz = rattle(atoms.cell.cartesian_positions(fxyz), stdev=self.interval / 3)
        grid_tree = cKDTree(xyz, copy_data=True)

        # 对atoms 在 xyz 方向超胞. Adapt from ase.geometry.geometry.general_find_mic
        ranges = [np.arange(-1 * p, p + 1) for p in atoms.pbc]
        hkls = np.array(list(itertools.product(*ranges)))
        vrvecs = hkls @ atoms.cell
        super_pos = np.concatenate(atoms.positions + vrvecs[:, None], axis=0)
        super_num = np.concatenate([atoms.numbers] * len(vrvecs))
        rsub = np.concatenate([self.rsub] * len(vrvecs))

        dist_max = coo_matrix((1, nx * ny * nz))
        atoms_num_type = set(atoms.numbers)
        # 对于不同的原子类型取不同的半径
        for num_type in atoms_num_type:
            pos = super_pos[super_num == num_type]
            atoms_tree = cKDTree(pos, copy_data=True)
            max_distance = self.rads + rsub[super_num == num_type][0]
            sdm = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=max_distance)
            # 保证没有格点的坐标跟grid 完全重合，如果有的话，需要标识出来，赋予它们另外的值，保证在后面识别中不为0。
            sdm0 = atoms_tree.sparse_distance_matrix(grid_tree, max_distance=0)
            for k in sdm0.keys():
                sdm[k] = 1
            dist_max = sdm.tocoo().nanmax(axis=0).maximum(dist_max)
        dist_max = dist_max.transpose().toarray()
        # 反转，距离大于 max_distance 的保留，其他的去掉
        points = xyz[dist_max[:,0]==0,:]
        self._grid = points

    @property
    def grid(self):
        if self._grid is None:
            self._generator()

        return self._grid

    def view(self):
        if len(self.grid) > 10000:
            print("Too much grid number, it will be very slow.")
        view(self.atoms + ase.Atoms(symbols=['X'] * len(self.grid), positions=self.grid))

    def get_grid_site_type(self, site_dict=None):
        """
        根据第一近邻原子返回格点所对应的类型
        :param site_dict: 格点的类型字典
            example: {0:((atom_num, count),(atom_num, count),...), ..., 'next_idx':int}
        :return: site label for each grid, site_dict
        """

        if site_dict is None:
            site_dict = {'next_idx': 0}
        _, Dga = get_distances(self.grid, self.atoms.positions, use_ase=True, cell=self.atoms.cell, pbc=self.atoms.pbc)
        Lga = (Dga - (self.rsub+self.rads)*1.1 < 0)  # 格点与原子的连接性。如果距离小于半径之和，则为不连接
        LTga = np.asarray([(Lga & (self.atoms.numbers==n1)).sum(-1) for n1 in self.atoms_num_type]).T  # 每个格点相连类矩阵
        label_T_set = sorted(set(tuple(i) for i in LTga))  # 以原子类型区分，不同格点的类别集合
        site_label = tuple(tuple((self.atoms_num_type[idx], l) for idx, l in enumerate(label)) for label in label_T_set)
        if site_dict is None:
            site_dict = {i:v for i,v in enumerate(site_label)}
            site_dict['next_idx'] = len(site_label)
        else:
            # 比较新旧字典，如果有新的，就加入到 site_dict 中
            old_site_label = tuple(v for k,v in site_dict.items() if type(k) == int)
            new_site = [i for i in site_label if i not in old_site_label]
            for ns in new_site:
                idx = site_dict['next_idx']
                site_dict[idx] = ns
                site_dict['next_idx'] = idx + 1
        site_dict_reverse = {tuple(iv[1] for iv in v):i for i,v in site_dict.items() if type(i)==int}
        grid_T_label = [site_dict_reverse[tuple(i)] for i in LTga]
        self.grid_site_type = grid_T_label
        self.site_type_dict = site_dict
        return grid_T_label, site_dict


def rattle(positions, stdev=0.001, rng=None, seed=None):
    """Rattle the grid to make the vector distribution more smooth.
    Adapt from ase.Atoms.rattle
    """
    if seed is not None and rng is not None:
        raise ValueError('Please do not provide both seed and rng.')
    if rng is None:
        if seed is None:
            seed = 42
        rng = np.random.RandomState(seed)
    return positions + rng.normal(scale=stdev, size=positions.shape)


def furthest_sites(points, n):
    # return the n sites that covers the max volume
    assert n < len(points)
    combs = list(itertools.combinations(range(len(points)), n))
    volumes = []
    if n==2:
        for c in combs:
            volumes.append(np.linalg.norm(points[c[0]] - points[c[1]]))
    elif n>2:
        for c in combs:
            pp = [points[i] for i in c]
            volumes.append(ConvexHull(pp).volume)
    idx = combs[np.argmax(volumes)]
    return idx
