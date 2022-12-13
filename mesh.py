import random

from double_sided_dict import DoubleSidedMap
from unique_vertices import unique_edges as calc_unique_edges, unique_vertices as calc_unique_vertices
from utils import return_value, replace_values_in_list


class Mesh:
    def __init__(self, data):
        self.vectors = data.vectors
        self.normals = data.normals
        self.edge_data = {}
        self.vertex_data = {}

    def __create_edge_map(self):
        self.edges_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in calc_unique_edges(self.vectors)},
            tuple
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

    def __create_vertex_map(self):
        self.vertices_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in calc_unique_vertices(self.vectors)},
            tuple
        )

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
        return 0

def translate_dict(from_dict, key_key_map, to_key_transformation=return_value):
    to_dict = {}
    for from_key, value in from_dict:
        to_key = key_key_map[from_key]
        to_dict[to_key] = value
    return to_dict
