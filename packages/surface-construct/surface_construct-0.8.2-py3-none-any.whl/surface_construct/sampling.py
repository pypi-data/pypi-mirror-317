"""
TODO: 关键点采样：top 位置、hollow位，bridge 位等等。
"""
import itertools
import numpy as np
from ase.geometry import get_distances
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from scipy.special import comb
from sklearn.cluster import KMeans as Cluster
import random

from surface_construct.utils import furthest_sites

MIN_HULL_ANGLE_COS = np.cos(np.pi * 30 / 180)

def hull_vertices(hull):
    hsimplices = hull.simplices
    hvertices = hull.vertices
    hnorms = hull.equations[:,0:-1]
    ndim = hsimplices.shape[1]
    vertices = []
    # 去掉 hull 的 simplices 的角度较大的点
    for i in hvertices:
        p0_facets_idx = np.argwhere(hsimplices == i)[:,0]
        p0_norms = hnorms[p0_facets_idx]
        cosangle = lambda a,b: a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
        # 求 i 凸点相邻的超平面的法向向量之间的夹角。如果存在夹角小于30度，即平面之间的夹角大于150度，则排除该点。反之，保留该点。
        norm_angle_cos = np.absolute([cosangle(a,b) for a,b in itertools.combinations(p0_norms, 2)])
        if np.sum(norm_angle_cos < MIN_HULL_ANGLE_COS) >= comb(ndim,2):
            vertices.append(i)

    return vertices


def addition_samples(sg_obj, size=None, probability=None, **kwargs):
    if 'seed' in kwargs:
        seed = kwargs['seed']
    else:
        seed = None
    if probability is None:
        probability = {
            "max_sigma": 0.2,  # 采样方法的概率
            "max_diversity": 0.8,
        }
    if size is None:
        size = 1

    # 归一化
    total = sum(probability.values())
    if total != 1.0:
        probability = {k: v / total for k, v in probability.items()}

    rng = np.random.default_rng(seed)
    method_list = rng.choice(list(probability.keys()), size=size, p=list(probability.values()))

    point_idx = np.array([], dtype=int)
    for method in method_list:
        method_lower = method.lower()
        if method_lower == 'max_sigma':
            sampling_obj = MaxSigmaSampling(sg_obj)
        elif method_lower == 'max_diversity':
            sampling_obj = MaxDiversitySampling(sg_obj)
        else:
            raise NotImplementedError
        point_idx = np.concatenate([point_idx, sampling_obj.samples(size=1, **kwargs)])  # 每种方法只采一个

    return point_idx


class SamplingBase:
    def __init__(self, sg_obj, **kwargs):
        self.sg_obj = sg_obj

    @property
    def _pop_size(self):
        return len(self.sg_obj.points)

    @property
    def _population(self):
        """
        默认的全体是 sg_obj.points 的 index
        :return:
        """
        return range(self._pop_size)

    def _append_sample_to_sg(self, point_idx=None):
        """
        将采样点加入到 sg_obj.sample_points 和相应的 vector

        :return:
        """
        if point_idx is not None:
            if self.sg_obj.sample_idx is not None:
                self.sg_obj.sample_idx = np.concatenate([self.sg_obj.sample_idx, point_idx])
                self.sg_obj._sample_vector = np.concatenate([self.sg_obj._sample_vector, self.sg_obj.vector[point_idx]])
                self.sg_obj.sample_points = np.concatenate([self.sg_obj.sample_points, self.sg_obj.points[point_idx]])
            else:
                self.sg_obj.sample_idx = np.array(point_idx)
                self.sg_obj._sample_vector = self.sg_obj.vector[point_idx]
                self.sg_obj.sample_points = self.sg_obj.points[point_idx]

    def _samples(self, size, **kwargs):
        raise NotImplementedError

    def samples(self, size=1, **kwargs):
        point_idx = self._samples(size=size, **kwargs)
        self._append_sample_to_sg(point_idx=point_idx)

        return point_idx


class KeyPointSampling(SamplingBase):
    """
    基本思路：先定位 hollow位，再根据图论分析定位 bridge 位，最后定位top位。第二步，筛选等价位点。
    需要一个基础func，从xy坐标，找到对应的格点。
    """
    def _samples(self, size, **kwargs):
        pass


class RandomSampling(SamplingBase):
    """
    完全随机的选择点，仅用于测试，效率太低。
    """

    def __init__(self, sg_obj, **kwargs):
        super().__init__(sg_obj, **kwargs)
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = None

    def _samples(self, size, **kwargs):
        rng = np.random.default_rng(self.seed)
        pop_idx = rng.choice(self._population, size=size)
        return pop_idx


class MaxSigmaSampling(SamplingBase):
    """
    对最大误差的点进行采样
    """

    def _samples(self, size, **kwargs):
        if 'energy' in self.sg_obj.grid_property:
            # 如果已经读入了一些能量，则返回误差最大的点
            idx = self.sg_obj.grid_property_sigma['energy'].argmax()
            return [idx]
        else:
            raise "No energy for all population, pls do initial sampling first!"


class InitialSampling(SamplingBase):
    """
    使用聚类-分层采样进行初始采样
    """

    def _samples(self, size, **kwargs):
        hull = ConvexHull(self.sg_obj.vector)
        #vertices = []
        # 去掉 hull 的 simplices 的角度较大的点
        #for i in hull.vertices:
        #    p1_idx, p2_idx = np.argwhere(hull.simplices == i)
        #    p0 = hull.points[i]
        #    p1 = hull.points[hull.simplices[p1_idx[0],1-p1_idx[1]]]
        #    p2 = hull.points[hull.simplices[p2_idx[0],1-p2_idx[1]]]
        #    a = p1 - p0
        #    b = p2 - p0
        #    cosangle = a.dot(b)/(np.linalg.norm(a) * np.linalg.norm(b))
        #    if cosangle > MIN_HULL_ANGLE_COS:
        #        vertices.append(i)
        # 聚类，vector_mesh
        vertices = hull_vertices(hull)
        n_vector_mesh = int(hull.volume / (self.sg_obj._vector_unit *
                                           self.sg_obj.interval)**self.sg_obj.vector.shape[1]) + 1
        cluster0 = Cluster(n_clusters=n_vector_mesh)
        cluster0.fit(self.sg_obj.vector)
        mesh_centers = cluster0.cluster_centers_
        self.sg_obj._mesh_centers = mesh_centers
        cluster = Cluster(n_clusters=size)
        cluster.fit(mesh_centers)
        self.sg_obj._clusters = cluster
        nvert = len(vertices)
        if nvert >= size:
            print(f"Warning: Sample number better be larger than {nvert}!")
            if size == 1:
                sample_idx = np.random.choice(vertices,1)
            elif size==nvert:
                sample_idx = vertices
            else:
                sample_idx = [vertices[i] for i in
                              furthest_sites(self.sg_obj.vector[vertices], size)]
        else:
            # 聚类
            cluster2 = Cluster(n_clusters=size-nvert)
            cluster2.fit(mesh_centers)
            center_dist = cdist(cluster2.cluster_centers_, self.sg_obj.vector)  # 计算每个点到中心的距离
            sample_idx = vertices + np.argmin(center_dist, axis=-1).tolist()
        return sample_idx

    def _append_sample_to_sg(self, point_idx=None):
        """
        将采样点加入到 sg_obj.sample_points 和相应的 vector
        :return:
        """
        if point_idx is not None:
            self.sg_obj.sample_idx = np.asarray(point_idx)
            self.sg_obj._sample_vector = self.sg_obj.vector[point_idx]
            self.sg_obj.sample_points = self.sg_obj.points[point_idx]


class MaxDiversitySampling(SamplingBase):
    """
    对当前采样结构差异最大的点进行采样
    基本思路是这样的：
        * 重新进行聚类，
        * 判断已经采样点属于的类别，找出没有点的类别，空类
        * 如果空类不止一个，比较这些空类中心与旧点的距离，选择距离最大的点。
    """

    def _samples(self, size, center=False, **kwargs):
        """

        :param size:
        :param center: 是否取中心。如果不是，则取能量最小值的点。如果没有能量则报错。
        :param kwargs:
        :return:
        """
        # 判断是否有过往的采样点，如果没有，调用 InitialSampling
        if self.sg_obj.sample_idx is None:
            raise "Please add initial samples (e.g. InitialSampling) before invoke this method!"
        cluster_size = len(self.sg_obj.sample_idx) + size
        nvirgin = 0
        larger_clusters = None
        larger_virgin = None
        virgin = None
        clusters = None
        # 如果等于则停止，并保存 cluster
        while nvirgin != size:
            # 以 len(sample_idx) + size 作为新的聚类的size
            clusters = Cluster(n_clusters=cluster_size).fit(self.sg_obj.vector)
            labels = clusters.labels_[self.sg_obj.sample_idx]
            labels_set = set(labels)
            virgin = set(range(cluster_size)) - labels_set
            nvirgin = len(virgin)
            # 判断分类以后空类数目与size的大小
            # 如果大于size，则减小size，并记录空类的数目
            if nvirgin > size:
                cluster_size -= 1
                larger_clusters = clusters
                larger_virgin = virgin
            # 如果小于 size 则增大size，检查上一个size是否有记录，如果有记录则使用上个size 的记录。从中随机选择size个点作为采样点。
            elif nvirgin < size:
                cluster_size += 1
                if larger_clusters is not None:
                    clusters = larger_clusters
                    virgin = larger_virgin
                    break
        # 从 virgin 里面选取 size 个点
        rng = np.random.default_rng()
        cluster_idx = rng.choice(list(virgin), size=size)
        if center:
            # 取中心位置的格点
            centers = clusters.cluster_centers_[cluster_idx]
            center_dist = cdist(centers, self.sg_obj.vector)  # 计算每个点到中心的距离
            point_idx = np.argmin(center_dist, axis=-1)
        else:
            # 取这些 clusters 中能量最小值点
            point_idx = []
            for c_id in cluster_idx:
                p_idx = np.arange(len(self.sg_obj.points))[clusters.labels_ == c_id]
                # 求这些点的能量最小值
                if 'energy' not in self.sg_obj.grid_property:
                    raise NotImplementedError
                p_energy = self.sg_obj.grid_energy[p_idx]
                point_idx.append(p_idx[p_energy.argmin()])

        return point_idx


class NewtonSampling(SamplingBase):
    """
    沿着受力方向进行采样
    """

    def _samples(self, size, **kwargs):
        raise NotImplementedError


class RandomWalk(SamplingBase):
    """
    从给定点出发随机行走进行采样
    """

    def __init__(self, sg_obj=None, probability=1.0, **kwargs):
        super().__init__(sg_obj, probability, **kwargs)

    def _samples(self, size, **kwargs):
        raise NotImplementedError


class SystematicSampling(SamplingBase):
    """
    等距采样。主要用于测试。
    """

    def _samples(self, size, **kwargs):
        if 'start' in kwargs:
            start = kwargs['start']
        else:
            start = random.randint(0, self._pop_size)
        stop = self._pop_size
        indices = list(range(start, stop)) + list(range(0, start))
        step = int(self._pop_size / size)
        point_idx = [indices[i + n * step] for n, i in enumerate(range(size))]

        return point_idx
