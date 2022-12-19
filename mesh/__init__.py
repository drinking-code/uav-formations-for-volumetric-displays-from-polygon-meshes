import random
from pprint import pprint

from double_sided_dict import DoubleSidedMap
from mesh.dedupe import dedupe_verts_in_faces
from unique_vertices import unique_edges as calc_unique_edges, unique_vertices as calc_unique_vertices
from utils import return_value, recursive_list, recursive_tuple


class Mesh:
    def __init__(self, data):
        self.faces = recursive_list(data.vectors)
        self.normals = recursive_list(data.normals)

        self.vertices = calc_unique_vertices(self.faces)
        self.vertices_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in self.vertices},
            tuple
        )
        # some vertices have multiple existence, i.e. different lists (instances) with same values
        dedupe_verts_in_faces(self.vertices_map, self.faces)

        self.edges = calc_unique_edges(self.faces)
        self.edges_map = DoubleSidedMap(
            {random.randint(0, 2 ** 32): edge for edge in self.edges},
            recursive_tuple
        )

        self.vertex_data = {}
        self.edge_data = {}

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
        self.edge_data[key] |= translate_dict(dictionary, self.edges_map.value_key)

    def get_edge_data(self, key):
        """
        :param key:
        :return: dict with edge (tuple of two tuple-vertices) as keys
        """
        return translate_dict(self.edge_data[key], self.edges_map.key_value, recursive_tuple)

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

    from .mesh_vector_manipulation import move_vertex, replace_vertices
    from .find_entries import find_vertex


def translate_dict(from_dict, key_key_map, to_key_transformation=return_value):
    to_dict = {}
    for from_key, value in from_dict.items():
        to_key = key_key_map[from_key]
        to_dict[to_key_transformation(to_key)] = value
    return to_dict
