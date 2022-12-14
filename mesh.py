import random
from pprint import pprint

from double_sided_dict import DoubleSidedMap
from unique_vertices import unique_edges as calc_unique_edges, unique_vertices as calc_unique_vertices
from utils import return_value, replace_values_in_list, recursive_list, recursive_tuple


class Mesh:
    def __init__(self, data):
        self.faces = recursive_list(data.vectors)
        self.edges = calc_unique_edges(self.faces)
        self.vertices = calc_unique_vertices(self.faces)
        self.normals = recursive_list(data.normals)

        self.vertex_data = {}
        self.edge_data = {}

        self.vertices_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in self.vertices},
            tuple
        )
        self.edges_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in self.edges},
            recursive_tuple
        )

    def set_edge_data(self, dictionary, key, merge=True):
        """
        :param dictionary: dict with edge (tuple of two tuple-vertices) as keys
        :param key:
        :param merge: Set False if all previous data should be erased
        :return:
        """
        if merge is False:
            self.edge_data[key].clear()
        if key not in self.edge_data:
            self.edge_data[key] = {}
        self.edge_data[key] = translate_dict(dictionary, self.edges_map.value_key)

    def get_edge_data(self, key):
        """
        :param key:
        :return: dict with edge (tuple of two tuple-vertices) as keys
        """
        return translate_dict(self.edge_data[key], self.edges_map.key_value, tuple)

    def set_vertex_data(self, dictionary, key, merge=True):
        """
        :param dictionary: dict with edge (tuple of two tuple-vertices) as keys
        :param key:
        :param merge: Set False if all previous data should be erased
        :return:
        """
        if merge is False:
            self.vertex_data[key].clear()
        if key not in self.vertex_data:
            self.vertex_data[key] = {}
        self.vertex_data[key] |= translate_dict(dictionary, self.vertices_map.value_key)

    def get_vertex_data(self, key):
        """
        :param key:
        :return: dict with edge (tuple of two tuple-vertices) as keys
        """
        return translate_dict(self.vertex_data[key], self.vertices_map.key_value, tuple)

    def move_vector(self, vector, target):
        vector_key = self.vertices_map[vector]
        vector_ref = self.vertices_map[vector_key]
        replace_values_in_list(vector_ref, target)
        # reassign new value
        self.vertices_map[vector_key] = vector_ref

    def replace_vectors(self, vectors, target):
        # find and remove edges between given vectors
        # find edges that contain one of the given vectors -> interpolate values
        vectors = recursive_list(vectors)
        edges_in_vector_group = []
        for index, vector_a in enumerate(vectors):
            for vector_b in vectors[index:]:
                edge_key = None
                if [vector_a, vector_b] in self.edges_map:
                    edge_key = self.edges_map[[vector_a, vector_b]]
                if [vector_b, vector_a] in self.edges_map:
                    edge_key = self.edges_map[[vector_b, vector_a]]
                if edge_key is None:
                    continue
                edges_in_vector_group.append(edge_key)
                for key in self.edge_data:
                    del self.edge_data[key][edge_key]

        edges_half_in_vector_group = {}
        for edge_id, edge_key in self.edges_map:
            edge_key = list(edge_key)
            existing_vector_filter = list(filter(lambda vertex: vertex in vectors, edge_key))
            if len(existing_vector_filter) != 1:
                continue
            edge_vector_outside_vectors = list(filter(lambda vertex: vertex is not existing_vector_filter[0], edge_key))[0]
            edge_vector_outside_vectors_tuple = tuple(edge_vector_outside_vectors)
            if edge_vector_outside_vectors_tuple not in edges_half_in_vector_group:
                edges_half_in_vector_group[edge_vector_outside_vectors_tuple] = []
            edges_half_in_vector_group[edge_vector_outside_vectors_tuple].append(edge_key)

        pprint(edges_half_in_vector_group)


def translate_dict(from_dict, key_key_map, to_key_transformation=return_value):
    to_dict = {}
    for from_key, value in from_dict.items():
        to_key = key_key_map[from_key]
        to_dict[to_key_transformation(to_key)] = value
    return to_dict
