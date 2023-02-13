from __future__ import annotations
from typing import TYPE_CHECKING

from pprint import pprint

import numpy as np

if TYPE_CHECKING:
    from . import Mesh
from utils import list_contains, find_in_iterable


def replace_vertices(self: Mesh, vertices_group, target):
    target = list(target)
    if list_contains(vertices_group, target):
        raise NotImplementedError('Group of vertices cannot be replaced with one of itself.')

    vertices_group_idents = [self.vertices_map[vertex] for vertex in vertices_group]
    hashable_vertex = self.vertices_map.make_hashable
    hashable_edge = self.edges_map.make_hashable

    # add target vertex to mesh
    self.vertices.append(target)
    target_id = self.id_from_coordinates(target)
    self.vertices_map[target_id] = target

    # interpolate data of the vertices in "vertices_group" to find the new datapoint of "target"
    for data_key in self.vertex_data:
        new_value = np.average([self.get_vertex_data(data_key)[hashable_vertex(vertex)] for vertex in vertices_group])
        self.set_vertex_data({hashable_vertex(target): new_value}, data_key)

    def n_vertices_in_vertices_group(vertex_set):
        vertices_shared_with_vertices_group = \
            filter(lambda vertex: list_contains(vertices_group_idents, vertex), vertex_set)
        return len(list(vertices_shared_with_vertices_group))

    # interpolate data of the edges that will be merged in this operation to find the data point of the merged edge
    # (edges containing exactly one vertex from "vertices_group")
    edges_common_vertex = {}
    for edge in self._edges:
        edge = tuple(edge)
        is_in_group = [list_contains(vertices_group_idents, vertex) for vertex in edge]
        if not any(is_in_group) or all(is_in_group):
            continue
        vertex_not_in_group = edge[is_in_group.index(False)]
        if vertex_not_in_group not in edges_common_vertex:
            edges_common_vertex[vertex_not_in_group] = []
        edges_common_vertex[vertex_not_in_group].append(edge)

    merged_edges_data = {}
    for vertex, edges in edges_common_vertex.items():
        merged_edges_data[vertex] = {
            data_key: np.average([self.get_edge_data(data_key)[edge] for edge in edges])
            for data_key in self.edge_data
        }

    # delete faces that contain more than one vertex from "vertices_group" will vanish
    faces_to_delete = []
    find_in_iterable(self._faces, lambda face: n_vertices_in_vertices_group(face) >= 2, faces_to_delete.append, True)
    faces_to_delete.reverse()
    for face in faces_to_delete:
        del self._faces[self._faces.index(face)]

    # bring the vertices to delete in the correct order to delete them
    vertices_to_delete = []
    find_in_iterable(self.vertices, lambda vertex: list_contains(vertices_group, vertex),
                     vertices_to_delete.append, True)
    vertices_to_delete.reverse()
    for vertex in vertices_to_delete:
        del self.vertices_map[vertex]
        del self.vertices[self.vertices.index(vertex)]

    # connect target vertex (replace all vertices in "vertices_group" with "target")
    for face in self._faces:
        face_list = list(face)
        is_in_group = [list_contains(vertices_group_idents, vertex) for vertex in face_list]
        if not (np.sum(is_in_group) == 1):
            continue
        vertex_in_group = face_list[is_in_group.index(True)]
        face.remove(vertex_in_group)
        face.add(target_id)

    # rebuild edge list, and edges map
    self.generate_edges_list()

    # insert new (interpolated) data for vertex and edges
    for vertex, data in merged_edges_data.items():
        edge_id = self.edges_map[(vertex, target_id)]
        edge_tuple_in_correct_order = hashable_edge(self.edges_map[edge_id])
        for data_key, value in data.items():
            self.set_edge_data({edge_tuple_in_correct_order: value}, data_key)

    # todo: garbage collect vertices data, edge data
