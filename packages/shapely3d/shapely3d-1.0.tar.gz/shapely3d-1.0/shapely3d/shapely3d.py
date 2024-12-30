# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 下午4:19
# @Author  : hhacai
# @File    : shapely3d.py
# @Software: PyCharm

import copy
from abc import ABC, abstractmethod
from shapely.wkt import loads
from shapely.ops import unary_union, substring, nearest_points
from shapely.affinity import rotate, scale
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, MultiPoint, LinearRing, \
    MultiLineString, GeometryCollection
from shapely.geometry.base import CAP_STYLE, JOIN_STYLE
import numpy as np
import numba

DEFAULT_Z = 0
GEOMTYPE_2D = '2D'
GEOMTYPE_3D = '3D'


class BaseGeometry3D(BaseGeometry, ABC):

    @property
    @abstractmethod
    def avg_z(self):
        pass

    @property
    @abstractmethod
    def priority(self):
        pass

    @property
    @abstractmethod
    def get_hash_tree(self):
        pass

    @property
    def geom_2d(self):
        return ops3D.trans_3d_2d(self)

    @abstractmethod
    def reset_z(self, z):
        pass

    @property
    def is_valid(self):
        if self.geom_2d.is_valid and self.geometryType() in ['Point3D', 'MultiPoint3D', 'LineString3D',
                                                             'MultiLineString3D', 'Polygon3D', 'MultiPolygon3D']:
            return True
        else:
            return False

    @property
    def centroid(self):
        center_point = super().centroid
        center_point_3d = Point3D(center_point)
        center_point_3d.reset_z(self.avg_z)
        return center_point_3d

    @property
    def convex_hull(self):
        convex_geom = super().convex_hull
        if convex_geom.geometryType() == 'Point':
            convex_geom_3d = Point3D(convex_geom)
        elif convex_geom.geometryType() == 'LineString':
            convex_geom_3d = LineString3D(convex_geom)
        else:
            convex_geom_3d = Polygon3D(convex_geom)
        convex_geom_3d.reset_z(self.avg_z)
        return convex_geom_3d

    @staticmethod
    def get_nearest_z(coords, p):
        xy_coords = coords[:, :2]
        z_coords = coords[:, 2]
        p_array = np.array(p)
        distance = np.linalg.norm(xy_coords - p_array, axis=1) + 1E-6
        weight = 1.0 / distance
        norm_weight = weight / weight.sum()
        avg_z = (z_coords * norm_weight).sum()
        return avg_z
        # if np.min(distance) > 20:
        #     return np.mean(coords, axis=0)[2]
        # else:
        #     min_index = np.argmin(distance)
        #     return coords[min_index][2]
        # _, index = date_tree.query(p, k=1, distance_upper_bound=20)
        # if index >= len(date_tree.data):
        #     return np.mean(list(hash_dict.values()))
        # else:
        #     nearest_p = date_tree.data[index]
        #     z = hash_dict[tuple(nearest_p.tolist())]
        #     return z

    def buffer(self, distance, resolution=16, quadsegs=None, cap_style=CAP_STYLE.round, join_style=JOIN_STYLE.round,
               mitre_limit=5.0, single_sided=False):
        this_z = self.avg_z
        buffer_geom = self.geom_2d.buffer(distance, resolution, quadsegs, cap_style, join_style, mitre_limit,
                                          single_sided)
        buffer_geom_3d = ops3D.trans_2d_3d(buffer_geom, this_z)
        return buffer_geom_3d

    def union(self, other, simple_union=False):
        if self.is_empty:
            return other
        elif other.is_empty:
            return self
        elif simple_union:
            this_z = self.avg_z
            union_geom = self.geom_2d.union(other.geom_2d)
            if not union_geom.is_valid:
                union_geom = union_geom.buffer(0)
            union_geom_3d = ops3D.trans_2d_3d(union_geom, this_z)
            return union_geom_3d
        else:
            self_geoms = []
            self_single_geomtype = ''
            self_single_priority = 1
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
                    self_single_geomtype = geom.geometryType()
                    self_single_priority = geom.priority
            else:
                self_geoms.append(self)
                self_single_geomtype = self.geometryType()
                self_single_priority = self.priority
            other_geoms = []
            other_single_geomtype = ''
            other_single_priority = 1
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
                    other_single_geomtype = geom.geometryType()
                    other_single_priority = geom.priority
            else:
                other_geoms.append(other)
                other_single_geomtype = other.geometryType()
                other_single_priority = other.priority
            if self_single_geomtype != other_single_geomtype:
                union_geoms = self_geoms if self_single_priority > other_single_priority else other_geoms
                single_geomtype = self_single_geomtype if self_single_priority > other_single_priority else other_single_geomtype
            else:
                union_geoms = self_geoms + other_geoms
                single_geomtype = self_single_geomtype
            if single_geomtype == 'Point3D':
                return MultiPoint3D(union_geoms)
            elif single_geomtype == 'LineString3D':
                return MultiLineString3D(union_geoms)
            else:
                return MultiPolygon3D(union_geoms)

    def intersects(self, other, z_tolerance=3, raw_intersects=False, simple_intersects=False):
        if self.is_empty or other.is_empty:
            return False
        elif z_tolerance is None or raw_intersects:
            return super().intersects(other)
        elif simple_intersects:
            if z_tolerance is not None and self.distance_z(other) > z_tolerance:
                return False
            else:
                return super().intersects(other)
        else:
            self_geoms = []
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
            else:
                self_geoms.append(self)
            other_geoms = []
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
            else:
                other_geoms.append(other)
            is_intersects = False
            for self_geom in self_geoms:
                for other_geom in other_geoms:
                    if self_geom.intersects(other_geom, raw_intersects=True):
                        self_coords = self_geom.get_hash_tree
                        other_coords = other_geom.get_hash_tree
                        intersection_geom_2d = self_geom.intersection(other_geom, raw_intersects=True)
                        intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom_2d)
                        if intersection_geom_3d.is_empty:
                            continue
                        intersection_geom_type = intersection_geom_3d.geometryType()
                        self_z_list = []
                        other_z_list = []
                        if intersection_geom_type == 'Point3D':
                            inter_p = (intersection_geom_3d.coords[0][0], intersection_geom_3d.coords[0][1])
                            self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                            other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiPoint3D':
                            for sub_geom in intersection_geom_3d:
                                inter_p = (sub_geom.coords[0][0], sub_geom.coords[0][1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'LineString3D':
                            if not intersection_geom_3d.is_valid:
                                print('intersects valid warning {}'.format(intersection_geom_3d.wkt))
                                continue
                            # 找相交点
                            for p in intersection_geom_3d.coords:
                                inter_p = (p[0], p[1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiLineString3D':
                            # 找相交点
                            for sub_geom in intersection_geom_3d:
                                if not sub_geom.is_valid:
                                    print('intersects valid warning {}'.format(sub_geom.wkt))
                                    continue
                                for p in sub_geom.coords:
                                    inter_p = (p[0], p[1])
                                    self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                    other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'Polygon3D':
                            if not intersection_geom_3d.is_valid:
                                print('intersects valid warning {}'.format(intersection_geom_3d.wkt))
                                continue
                            for p in intersection_geom_3d.boundary.coords:
                                inter_p = (p[0], p[1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiPolygon3D':
                            self_z_list = []
                            other_z_list = []
                            for sub_geom in intersection_geom_3d:
                                if not sub_geom.is_valid:
                                    print('intersects valid warning {}'.format(sub_geom.wkt))
                                    continue
                                for p in sub_geom.boundary.coords:
                                    inter_p = (p[0], p[1])
                                    self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                    other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        else:
                            print("intersects type warning {}".format(intersection_geom_3d))
                            continue
                        self_z = sum(self_z_list) / len(self_z_list)
                        other_z = sum(other_z_list) / len(other_z_list)
                        if abs(self_z - other_z) < z_tolerance:
                            is_intersects = True
                            break
            return is_intersects

    def intersection(self, other, z_tolerance=3, raw_intersects=False, simple_intersection=False):
        if self.is_empty or other.is_empty:
            return Point3D()
        elif raw_intersects:
            # return super().intersection(other)
            return self.intersection_np(other)
        elif simple_intersection or z_tolerance is None:
            if z_tolerance is not None and self.distance_z(other) > z_tolerance:
                return Point3D()
            else:
                this_z = self.avg_z
                intersection_geom = self.intersection_np(other)
                intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom, this_z)
                return intersection_geom_3d
        else:
            self_geoms = []
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
            else:
                self_geoms.append(self)
            other_geoms = []
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
            else:
                other_geoms.append(other)
            intersection_geoms = []
            for self_geom in self_geoms:
                for other_geom in other_geoms:
                    intersection_geom_2d = self_geom.intersection(other_geom, raw_intersects=True)
                    intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom_2d)
                    if intersection_geom_3d.is_empty:
                        continue
                    intersection_geom_type = intersection_geom_3d.geometryType()
                    dst_intersection_geom = []
                    self_coords = self_geom.get_hash_tree
                    other_coords = other_geom.get_hash_tree
                    if intersection_geom_type == 'Point3D':
                        for p in intersection_geom_3d.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if len(dst_intersection_geom) == 0:
                            intersection_geoms.append(Point3D())
                        else:
                            intersection_geoms.append(Point3D(dst_intersection_geom[0]))
                    elif intersection_geom_type == 'MultiPoint3D':
                        for sub_geom in intersection_geom_3d:
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                dst_intersection_geom.append(Point3D())
                            else:
                                dst_intersection_geom.append(Point3D(tmp[0]))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'LineString3D':
                        if not intersection_geom_3d.is_valid:
                            print('intersects error {}'.format(intersection_geom_3d.wkt))
                            continue
                        delta_z_exam = True
                        for p in intersection_geom_3d.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                delta_z_exam = False
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if not delta_z_exam:
                            intersection_geoms.append(LineString3D())
                        else:
                            intersection_geoms.append(LineString3D(dst_intersection_geom))
                    elif intersection_geom_type == 'MultiLineString3D':
                        for sub_geom in intersection_geom_3d:
                            if not sub_geom.is_valid:
                                print('intersects error {}'.format(sub_geom.wkt))
                                continue
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                intersection_geoms.append(LineString3D())
                            else:
                                dst_intersection_geom.append(LineString3D(tmp))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'Polygon3D':
                        if not intersection_geom_3d.is_valid:
                            print('intersects error {}'.format(intersection_geom_3d.wkt))
                            continue
                        delta_z_exam = True
                        for p in intersection_geom_3d.boundary.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                delta_z_exam = False
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if not delta_z_exam:
                            intersection_geoms.append(Polygon3D())
                        else:
                            intersection_geoms.append(Polygon3D(dst_intersection_geom))
                    elif intersection_geom_type == 'MultiPolygon3D':
                        for sub_geom in intersection_geom_3d:
                            if not sub_geom.is_valid:
                                print('intersects error {}'.format(sub_geom.wkt))
                                continue
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.boundary.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                intersection_geoms.append(Polygon3D())
                            else:
                                dst_intersection_geom.append(Polygon3D(tmp))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'GeometryCollection3D':
                        print("intersection warning {}".format(intersection_geom_3d))
                        continue
                        # for sub_geom in intersection_geom_3d:
                        #     tmp = []
                        #     for p in sub_geom.coords:
                        #         inter_p = (p[0], p[1])
                        #         self_z = self.get_nearest_z(self_data_tree, self_hash_dict,self_coords,  inter_p)
                        #         tmp.append([p[0], p[1], self_z])
                        #     if sub_geom.geom_type == 'LineString':
                        #         dst_intersection_geom.append(LineString3D(tmp))
                        #     elif sub_geom.geom_type == 'Point':
                        #         dst_intersection_geom.append(Point3D(tmp[0]))
                        # return GeometryCollection3D(dst_intersection_geom)
                    else:
                        print("intersection warning {}".format(intersection_geom_3d))
                        continue
            result = ops3D.unary_union(intersection_geoms)
            return result

    def intersection_np(self, other):
        if self.geometryType() == "LineString3D" and other.geometryType() == "LineString3D":
            a_coords = np.array(self.coords)
            a_lines = []
            for i in range(a_coords.shape[0]):
                if i == 0:
                    continue
                a_lines.append([a_coords[i], a_coords[i - 1]])
            b_coords = np.array(other.coords)
            b_lines = []
            for i in range(b_coords.shape[0]):
                if i == 0:
                    continue
                b_lines.append([b_coords[i], b_coords[i - 1]])

            intersect_coords = []
            for a_line in a_lines:
                for b_line in b_lines:
                    a1, a2, b1, b2 = a_line[0][:2], a_line[1][:2], b_line[0][:2], b_line[1][:2]
                    a_minx, a_maxx = min(a1[0], a2[0]), max(a1[0], a2[0])
                    a_miny, a_maxy = min(a1[1], a2[1]), max(a1[1], a2[1])
                    b_minx, b_maxx = min(b1[0], b2[0]), max(b1[0], b2[0])
                    b_miny, b_maxy = min(b1[1], b2[1]), max(b1[1], b2[1])
                    avg_z = (a_line[0][2] + a_line[1][2] + b_line[0][2] + b_line[1][2]) / 4.0

                    da = a2 - a1
                    db = b2 - b1
                    dp = a1 - b1

                    dap = np.empty_like(da)
                    dap[0] = -da[1]
                    dap[1] = da[0]

                    denom = np.dot(dap, db)
                    num = np.dot(dap, dp)

                    if denom == 0:
                        pass
                    else:
                        result = (num / denom.astype(float)) * db + b1
                        result_x, result_y = result
                        if a_minx <= result_x <= a_maxx and b_minx <= result_x <= b_maxx and a_miny <= result_y <= a_maxy and b_miny <= result_y <= b_maxy:
                            intersect_coords.append([result_x, result_y, avg_z])
                        else:
                            pass

            if len(intersect_coords) == 0:
                return Point3D()
            elif len(intersect_coords) == 1:
                return Point3D(intersect_coords[0])
            else:
                return MultiPoint3D(intersect_coords)
        else:
            return super().intersection(other)

    def distance(self, other, z_tolerance=None):
        if self.is_empty or other.is_empty:
            return 0
        elif z_tolerance is None:
            if self.geometryType() == "Point3D" and other.geometryType() == "Point3D":
                return np.linalg.norm(np.array(self.coords[0])[:2] - np.array(other.coords[0])[:2])
            else:
                return super().distance(other)
        else:
            distance_2d = super().distance(other)
            z_distance = self.distance_z(other)
            if z_distance < z_tolerance:
                return distance_2d
            else:
                return distance_2d + z_distance

    def distance_z(self, other):
        if self.is_empty or other.is_empty:
            return 0
        elif ops3D.judge_2d_3d(self) == GEOMTYPE_2D or ops3D.judge_2d_3d(other) == GEOMTYPE_2D:
            return 0
        else:
            return abs(self.avg_z - other.avg_z)


class Point3D(BaseGeometry3D, Point):
    def __init__(self, *args):
        Point.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            Point.__init__(self, [self.x, self.y, DEFAULT_Z])

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            return self.z

    @property
    def priority(self):
        return 1

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # for p in self.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(self.coords)
        return np.array(self.coords)

    # @property
    # def is_empty(self):
    #     return self.empty_flag

    def geometryType(self):
        return "Point3D"

    def reset_z(self, z):
        Point3D.__init__(self, [self.x, self.y, z])


class LineString3D(BaseGeometry3D, LineString):
    def __init__(self, *args):
        LineString.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            self.reset_z(DEFAULT_Z)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            coords = np.array(list(self.coords))
            return float(np.mean(coords[:, 2]))

    @property
    def priority(self):
        return 2

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # for p in self.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(self.coords)
        return np.array(self.coords)

    def geometryType(self):
        return "LineString3D"

    def reset_z(self, z):
        bound_coords_3d = []
        bound_coords = list(self.coords)
        for bound_coord in bound_coords:
            bound_coords_3d.append([bound_coord[0], bound_coord[1], z])
        LineString3D.__init__(self, bound_coords_3d)

    def interpolate(self, distance, normalized=False):
        if self.is_empty:
            return self
        else:
            this_z = self.avg_z
            line_2d = ops3D.trans_3d_2d(self)
            inter_point_2d = line_2d.interpolate(distance, normalized)
            inter_point_3d = ops3D.trans_2d_3d(inter_point_2d)
            inter_point_3d.reset_z(this_z)
            return inter_point_3d

    def project(self, other, normalized=False):
        if self.is_empty or other.is_empty:
            return 0
        else:
            line_2d = ops3D.trans_3d_2d(self)
            other_2d = ops3D.trans_3d_2d(other)
            project_distance = line_2d.project(other_2d, normalized)
            return project_distance


class Polygon3D(BaseGeometry3D, Polygon):
    def __init__(self, *args):
        Polygon.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            self.reset_z(DEFAULT_Z)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            coords = np.array(list(self.boundary.coords))
            return float(np.mean(coords[:, 2]))

    @property
    def priority(self):
        return 3

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for p in self.boundary.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        #     coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for p in self.boundary.coords:
            coords.append(p)
        return np.array(coords)

    @property
    def boundary(self):
        boundary_line = super().boundary
        boundary_line = ops3D.trans_2d_3d(boundary_line)
        if boundary_line.geometryType() == 'MultiLineString3D':
            max_length = None
            exterior_line = boundary_line.geoms_3d[0]
            for line in boundary_line.geoms_3d:
                if max_length is None or line.length > max_length:
                    max_length = line.length
                    exterior_line = line
            return exterior_line
        else:
            return boundary_line

    def geometryType(self):
        return "Polygon3D"

    def reset_z(self, z):
        bound_coords_3d = []
        bound_coords = list(self.boundary.coords)
        for bound_coord in bound_coords:
            bound_coords_3d.append([bound_coord[0], bound_coord[1], z])
        Polygon3D.__init__(self, bound_coords_3d)


class MultiPoint3D(BaseGeometry3D, MultiPoint):
    def __init__(self, points=None):
        MultiPoint.__init__(self, points)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for point3d in self.geoms_3d:
                list_z.append(point3d.z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 4

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(Point3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiPoint3D"

    def reset_z(self, z):
        points = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            points.append(geom)
        self.__init__(points)


class MultiLineString3D(BaseGeometry3D, MultiLineString):
    def __init__(self, lines=None):
        MultiLineString.__init__(self, lines)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for line3d in self.geoms_3d:
                list_z.append(line3d.avg_z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 5

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(LineString3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiLineString3D"

    def reset_z(self, z):
        lines = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            lines.append(geom)
        self.__init__(lines)


class MultiPolygon3D(BaseGeometry3D, MultiPolygon):
    def __init__(self, polygons=None):
        MultiPolygon.__init__(self, polygons)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for polygon3d in self.geoms_3d:
                list_z.append(polygon3d.avg_z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 6

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(Polygon3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.boundary.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.boundary.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiPolygon3D"

    def reset_z(self, z):
        polygons = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            polygons.append(geom)
        self.__init__(polygons)


class wkt3D:
    @staticmethod
    def loads(data: str, z=None):
        geometry = loads(data)
        if geometry.geometryType() == 'Point':
            geometry_3d = Point3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        elif geometry.geometryType() == 'LineString':
            geometry_3d = LineString3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        elif geometry.geometryType() == 'Polygon':
            geometry_3d = Polygon3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        else:
            print("wkt format error: {}".format(data))
            return Point3D()


class ops3D:
    @staticmethod
    def trans_3d_2d(geom, retain_z=False):
        if ops3D.judge_2d_3d(geom) == GEOMTYPE_2D:
            return geom
        elif geom.geometryType() == 'Point3D':
            if geom.is_empty:
                geom_2d = Point()
            else:
                geom_2d = Point(geom.x, geom.y, geom.z) if retain_z else Point(geom.x, geom.y)
        elif geom.geometryType() == 'LineString3D':
            if geom.is_empty:
                geom_2d = LineString()
            else:
                geom_2d = LineString(np.array(list(geom.coords))) if retain_z else LineString(
                    np.array(list(geom.coords))[:, :2])
        elif geom.geometryType() == 'Polygon3D':
            if geom.is_empty:
                geom_2d = Polygon()
            else:
                geom_2d = Polygon(np.array(list(geom.boundary.coords))) if retain_z else Polygon(
                    np.array(list(geom.boundary.coords))[:, :2])
        elif geom.geometryType() == 'MultiPoint3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiPoint(geoms)
        elif geom.geometryType() == 'MultiLineString3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiLineString(geoms)
        elif geom.geometryType() == 'MultiPolygon3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiPolygon(geoms)
        else:
            print("trans_3d_2d format error: {}".format(geom.wkt))
            return Point()
        return geom_2d

    @staticmethod
    def trans_2d_3d(geom, z: float = None):
        if ops3D.judge_2d_3d(geom) == GEOMTYPE_3D:
            return geom
        elif geom.geometryType() == 'Point':
            if geom.is_empty:
                geom_3d = Point3D()
            else:
                geom_3d = Point3D(geom)
        elif geom.geometryType() == 'LineString':
            if geom.is_empty:
                geom_3d = LineString3D()
            else:
                geom_3d = LineString3D(geom)
        elif geom.geometryType() == 'Polygon':
            if geom.is_empty:
                geom_3d = Polygon3D()
            else:
                geom_3d = Polygon3D(geom)
        elif geom.geometryType() == 'MultiPoint':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(Point3D(geom_))
            geom_3d = MultiPoint3D(geoms)
        elif geom.geometryType() == 'MultiLineString':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(LineString3D(geom_))
            geom_3d = MultiLineString3D(geoms)
        elif geom.geometryType() == 'MultiPolygon':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(Polygon3D(geom_))
            geom_3d = MultiPolygon3D(geoms)
        else:
            print("trans_2d_3d format error: {}".format(geom.wkt))
            return Point3D()
        if z is not None and not geom_3d.is_empty:
            geom_3d.reset_z(z)
        return geom_3d

    @staticmethod
    def judge_2d_3d(geom):
        if '3D' in geom.geometryType():
            return GEOMTYPE_3D
        else:
            return GEOMTYPE_2D

    @staticmethod
    def unary_union(geoms: list, z: float = 0.0, simple_union=False):
        if len(geoms) == 0:
            return Polygon3D()
        elif simple_union:
            geoms_2d = []
            zs = []
            for geom in geoms:
                if ops3D.judge_2d_3d(geom) == GEOMTYPE_3D:
                    geoms_2d.append(ops3D.trans_3d_2d(geom))
                    zs.append(geom.avg_z)
                else:
                    geoms_2d.append(geom)
                    zs.append(z)
            union_geom = unary_union(geoms_2d)
            if union_geom.is_empty:
                return Polygon3D()
            else:
                avg_z = float(np.mean(zs))
                union_geom_3d = ops3D.trans_2d_3d(union_geom)
                union_geom_3d.reset_z(avg_z)
                return union_geom_3d
        else:
            union_geom = Polygon3D()
            for geom in geoms:
                union_geom = union_geom.union(geom)
            return union_geom

    @staticmethod
    def nearest_points(geom1, geom2):
        if ops3D.judge_2d_3d(geom1) == GEOMTYPE_3D:
            geom1_z = geom1.avg_z
            geom1 = ops3D.trans_3d_2d(geom1)
        else:
            geom1_z = 0.0
        if ops3D.judge_2d_3d(geom2) == GEOMTYPE_3D:
            geom2_z = geom2.avg_z
            geom2 = ops3D.trans_3d_2d(geom2)
        else:
            geom2_z = 0.0
        point1, point2 = nearest_points(geom1, geom2)
        point1_3d = ops3D.trans_2d_3d(point1, geom1_z)
        point2_3d = ops3D.trans_2d_3d(point2, geom2_z)
        return point1_3d, point2_3d

    @staticmethod
    def substring(geom: LineString3D, start_dist, end_dist, normalized=False):
        if normalized is False:
            start_norm_distance = start_dist * geom.length
            end_norm_distance = end_dist * geom.length
        else:
            start_norm_distance = start_dist
            end_norm_distance = end_dist
        xy_line = LineString(np.array(list(geom.coords))[:, :2])
        yz_line = LineString(np.array(list(geom.coords))[:, 1:])
        sub_xy_line = substring(xy_line, start_norm_distance, end_norm_distance, normalized)
        sub_yz_line = substring(yz_line, start_norm_distance, end_norm_distance, normalized)
        sub_xy_coords = np.array(list(sub_xy_line.coords))[:, :2]
        sub_z_coords = np.array(list(sub_yz_line.coords))[:, -1]
        sub_z_coords = np.interp(np.linspace(0, sub_z_coords.shape[0] - 1, num=sub_xy_coords.shape[0], endpoint=True),
                                 np.linspace(0, sub_z_coords.shape[0] - 1, num=sub_z_coords.shape[0], endpoint=True),
                                 sub_z_coords)
        sub_line = LineString3D(np.append(sub_xy_coords, sub_z_coords[:, np.newaxis], axis=1))
        return sub_line

    @staticmethod
    def interpolate(geom: LineString3D, interp_dist, normalized=False):
        if not normalized:
            interp_norm = interp_dist / geom.length
        else:
            interp_norm = interp_dist
        start_coord = np.array(geom.coords[0])
        end_coord = np.array(geom.coords[-1])
        interp_x = start_coord[0] + (end_coord[0] - start_coord[0]) * interp_norm
        interp_y = start_coord[1] + (end_coord[1] - start_coord[1]) * interp_norm
        interp_z = start_coord[2] + (end_coord[2] - start_coord[2]) * interp_norm
        return Point3D(interp_x, interp_y, interp_z)


class ops3D_smp:
    @staticmethod
    def geom_to_array(geom):
        if geom.geometryType() == 'Point3D':
            return np.array(geom.coords)[0]
        else:
            return np.array(geom.coords)

    @staticmethod
    @numba.jit(nopython=True)
    def distance_point_point(point_1, point_2):
        vector = point_1 - point_2
        dis = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        return dis

    @staticmethod
    @numba.jit(nopython=True)
    def interpolate(line, interp_dist, normalized=False):
        start_coord, end_coord = line[0], line[-1]
        line_vector = end_coord - start_coord
        line_length = np.sqrt(line_vector[0] ** 2 + line_vector[1] ** 2)
        if not normalized:
            interp_norm = interp_dist / line_length
        else:
            interp_norm = interp_dist
        new_point = start_coord + line_vector * interp_norm
        return new_point

    @staticmethod
    @numba.jit(nopython=True)
    def points_line_distance(points, line):
        points = points[:, :2]
        line = line[:, :2]
        start, end = line[0], line[-1]
        vector_base = end - start
        module_base = np.sqrt(vector_base[0] ** 2 + vector_base[1] ** 2)
        vector_new = points - start
        cross = np.dot(vector_base, vector_new.T)
        # 垂足在线段内的位置
        t = cross / module_base ** 2
        # 垂足到点的距离
        vectors_result = start + (vector_base.reshape(-1, 2).T * t).T - points
        distance = np.sqrt(vectors_result[:, 0] ** 2 + vectors_result[:, 1] ** 2)
        # distance = np.linalg.norm(start + (vector_base.reshape(-1, 2).T * t).T - points, axis=1)
        # 修正线段外的垂足距离
        vectors_start_outlier = points[np.logical_or(t < 0, t > 1)] - start
        vectors_end_outlier = points[np.logical_or(t < 0, t > 1)] - end
        start_outlier_distance = np.sqrt(vectors_start_outlier[:, 0] ** 2 + vectors_start_outlier[:, 1] ** 2)
        end_outlier_distance = np.sqrt(vectors_end_outlier[:, 0] ** 2 + vectors_end_outlier[:, 1] ** 2)
        start_outlier_distance[end_outlier_distance < start_outlier_distance] = end_outlier_distance[
            end_outlier_distance < start_outlier_distance]
        distance[np.logical_or(t < 0, t > 1)] = start_outlier_distance
        return distance

    @staticmethod
    def polygon_contains_point(polygon_coords, point):
        def isRayIntersectsSegment(poi, s_poi, e_poi):  # [x,y] [lng,lat]
            # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
            if s_poi[1] == e_poi[1]:  # 排除与射线平行、重合，线段首尾端点重合的情况
                return False
            if s_poi[1] > poi[1] and e_poi[1] > poi[1]:  # 线段在射线上边
                return False
            if s_poi[1] < poi[1] and e_poi[1] < poi[1]:  # 线段在射线下边
                return False
            if s_poi[1] == poi[1] and e_poi[1] > poi[1]:  # 交点为下端点，对应spoint
                return False
            if e_poi[1] == poi[1] and s_poi[1] > poi[1]:  # 交点为下端点，对应epoint
                return False

            xseg = e_poi[0] - (e_poi[0] - s_poi[0]) * (e_poi[1] - poi[1]) / (e_poi[1] - s_poi[1])  # 求交
            if xseg < poi[0]:  # 交点在射线起点的左侧
                return False
            return True  # 排除上述情况之后

        sinsc = 0  # 交点个数
        for i in range(len(polygon_coords) - 1):  # 循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
            s_poi = polygon_coords[i]
            e_poi = polygon_coords[i + 1]
            if isRayIntersectsSegment(point, s_poi, e_poi):
                sinsc += 1  # 有交点就加1
        return True if sinsc % 2 == 1 else False


class affinity3D:
    @staticmethod
    def rotate(geom, angle, origin='center', use_radians=False):
        geom_2d = ops3D.trans_3d_2d(geom, retain_z=True)
        if isinstance(origin, str):
            origin_2d = origin
        else:
            origin_2d = ops3D.trans_3d_2d(origin, retain_z=True)
        rot_geom_2d = rotate(geom_2d, angle, origin=origin_2d, use_radians=use_radians)
        rot_geom_3d = ops3D.trans_2d_3d(rot_geom_2d)
        return rot_geom_3d

    @staticmethod
    def scale(geom, xfact=1.0, yfact=1.0, zfact=1.0, origin='center'):
        geom_2d = ops3D.trans_3d_2d(geom, retain_z=True)
        if isinstance(origin, str):
            origin_2d = origin
        else:
            origin_2d = ops3D.trans_3d_2d(origin, retain_z=True)
        scale_geom_2d = scale(geom_2d, xfact=xfact, yfact=yfact, zfact=zfact, origin=origin_2d)
        scale_geom_3d = ops3D.trans_2d_3d(scale_geom_2d)
        return scale_geom_3d


if __name__ == '__main__':
    import math
    import time

    # start_time = time.perf_counter_ns()
    # a = Point3D(2, 2, 2)
    # b = Point3D(6, 6, 6)
    # distance = a.distance(b)
    # print(time.perf_counter_ns() - start_time)
    # start_time = time.perf_counter_ns()
    # if a.geometryType() == "Point3D" and b.geometryType() == "Point3D":
    #     a_np = np.array(a.coords[0])
    #     b_np = np.array(b.coords[0])
    #     distance = np.linalg.norm(a_np - b_np)
    # print(time.perf_counter_ns() - start_time)

    p = Point3D()

    a = LineString3D([[0, 0, 1], [1, 1, 1], [2, 2, 1]])
    b = LineString3D([[0, 1, 1], [1, 0, 1]])

    start_time = time.perf_counter_ns()

    for _ in range(100):
        c = a.intersection(b)
    print(time.perf_counter_ns() - start_time)

    start_time = time.perf_counter_ns()
    for _ in range(100):
        a_coords = np.array(a.coords)
        a_lines = []
        for i in range(a_coords.shape[0]):
            if i == 0:
                continue
            a_lines.append([a_coords[i], a_coords[i - 1]])
        b_coords = np.array(b.coords)
        b_lines = []
        for i in range(b_coords.shape[0]):
            if i == 0:
                continue
            b_lines.append([b_coords[i], b_coords[i - 1]])

        intersect_coords = []
        for a_line in a_lines:
            for b_line in b_lines:
                a1, a2, b1, b2 = a_line[0], a_line[1], b_line[0], b_line[1]
                a_minx, a_maxx = min(a1[0], a2[0]), max(a1[0], a2[0])
                a_miny, a_maxy = min(a1[1], a2[1]), max(a1[1], a2[1])
                b_minx, b_maxx = min(b1[0], b2[0]), max(b1[0], b2[0])
                b_miny, b_maxy = min(b1[1], b2[1]), max(b1[1], b2[1])
                avg_z = (a1[2] + a2[2] + b1[2] + b2[2]) / 4.0

                da = a2 - a1
                db = b2 - b1
                dp = a1 - b1

                dap = np.empty_like(da)
                dap[0] = -da[1]
                dap[1] = da[0]

                denom = np.dot(dap, db)
                num = np.dot(dap, dp)

                if denom == 0:
                    pass
                else:
                    result = (num / denom.astype(float)) * db + b1
                    result_x, result_y, result_z = result
                    if a_minx <= result_x <= a_maxx and b_minx <= result_x <= b_maxx and a_miny <= result_y <= a_maxy and b_miny <= result_y <= b_maxy:
                        intersect_coords.append([result_x, result_y, avg_z])
                    else:
                        pass

        if len(intersect_coords) == 0:
            rr = Point3D()
        elif len(intersect_coords) == 1:
            rr = Point3D(intersect_coords[0])
        else:
            rr = MultiPoint3D(intersect_coords)
        k = 0

    print(time.perf_counter_ns() - start_time)

    print('develop test')
