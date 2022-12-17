from pprint import pprint

import numpy as np

from mesh.dedupe_verts_in_faces import dedupe_verts_in_edges, dedupe_verts_in_faces
from utils import replace_values_in_list, recursive_list, zip_common, recursive_tuple, list_contains


def move_vertex(self, vertex, target):
    def edge_has_vertex(edge):
        return list_contains(recursive_list(edge), vertex)

    # get refs to vertex and delete key (baked tuple)
    vertex_key = self.vertices_map[vertex]
    vertex_ref = self.vertices_map[vertex_key]
    del self.vertices_map[vertex_key]
    # get edges with vertex and delete keys (baked tuples)
    edges_with_vertex = self.edges_map.find_by_value(edge_has_vertex, True)
    for edge_key in edges_with_vertex.keys():
        del self.edges_map[edge_key]

    # change vertex values
    replace_values_in_list(vertex_ref, target)

    # reassign new vertex
    self.vertices_map[vertex_key] = vertex_ref
    # reassign new edges
    for edge_key, edge_ref in edges_with_vertex.items():
        self.edges_map[edge_key] = edge_ref


def replace_vertices(self, vertices, target):
    # find and remove edges between given vectors
    vertices = recursive_list(vertices)
    edges_in_vector_group = []

    def interpolate_and_delete_data(data_source, key_id_map, value_keys):
        values = {
            data_key: [
                data_source[data_key][key_id_map[value_key]]
                for value_key in value_keys
            ] for data_key in data_source
        }
        interpolated = {
            data_key: np.average(values[data_key])
            for data_key in values
        }
        for data_key in data_source:
            for value_key in value_keys:
                del data_source[data_key][key_id_map[value_key]]
        return interpolated

    vectors_interpolated = interpolate_and_delete_data(self.vertex_data, self.vertices_map, vertices)

    for index, vertex_a in enumerate(vertices):
        for vertex_b in vertices[index:]:
            edge = None
            if [vertex_a, vertex_b] in self.edges_map:
                edge = self.edges_map[[vertex_a, vertex_b]]
            if [vertex_b, vertex_a] in self.edges_map:
                edge = self.edges_map[[vertex_b, vertex_a]]
            if edge is None:
                continue
            edges_in_vector_group.append(edge)
            for key in self.edge_data:
                del self.edge_data[key][edge]

    # find edges that contain one of the given vectors -> interpolate values
    edges_half_in_vector_group = {}
    for edge_id, edge in self.edges_map:
        edge = list(edge)
        edge = self.edges_map[self.edges_map[edge]]
        existing_vector_filter = list(filter(lambda vertex: vertex in vertices, edge))
        if len(existing_vector_filter) != 1:
            continue
        edge_vector_outside_vectors = list(filter(lambda vertex: vertex is not existing_vector_filter[0], edge))[0]
        edge_vector_outside_vectors_tuple = tuple(edge_vector_outside_vectors)
        if edge_vector_outside_vectors_tuple not in edges_half_in_vector_group:
            edges_half_in_vector_group[edge_vector_outside_vectors_tuple] = []
        edges_half_in_vector_group[edge_vector_outside_vectors_tuple].append(edge)

    edges_half_in_vector_group_values = {}
    for edge_vector_outside_vectors, edges in edges_half_in_vector_group.items():
        edges_interpolated = interpolate_and_delete_data(self.edge_data, self.edges_map, edges)
        edges_half_in_vector_group_values[edge_vector_outside_vectors] = edges_interpolated

    for vertex in vertices:
        self.move_vertex(vertex, target)

    # dedupe (only keep one key from vertices)
    dedupe_verts_in_faces(self.vertices_map, self.faces)
    dedupe_verts_in_edges(self.vertices_map, self.edges)

    # set new interpolated data
    for key in vectors_interpolated:
        self.set_vertex_data({tuple(self.vertices_map[self.vertices_map[target]]): vectors_interpolated[key]}, key)

    for key in list(edges_half_in_vector_group_values.values())[0]:
        new_edge_data = {}
        for edge_vector_outside_vectors, edges, data \
                in zip_common(edges_half_in_vector_group, edges_half_in_vector_group_values):
            for edge in edges:
                new_edge_data[recursive_tuple(edge)] = data[key]
        self.set_edge_data(new_edge_data, key)
