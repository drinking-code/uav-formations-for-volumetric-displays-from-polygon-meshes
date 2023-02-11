from pprint import pprint

from double_sided_dict import DoubleSidedMap
from unique_vertices import unique_edges as calc_unique_edges, unique_vertices as calc_unique_vertices
from utils import return_value, recursive_list, recursive_tuple


def id_from_coordinates(coordinates):
    ident = 0
    for index, vertex in enumerate(coordinates):
        ident += (index + 2) ** vertex
    return ident


class Mesh:
    def __init__(self, data):
        faces = recursive_list(data.vectors)
        self.vertices = calc_unique_vertices(faces)
        self.vertices_map: DoubleSidedMap = DoubleSidedMap(
            {id_from_coordinates(vertex): vertex for vertex in self.vertices},
            tuple
        )

        self._faces: list[set] = []
        for face in faces:
            face_ref = set()
            for vertex in face:
                face_ref.add(self.vertices_map[vertex])
            self._faces.append(face_ref)

        self._edges = None
        self.edges_map = None
        self.generate_edges_list()

        self.vertex_data = {}
        self.edge_data = {}

    def generate_edges_list(self):
        self._edges = calc_unique_edges(self._faces)
        self.edges_map: DoubleSidedMap = DoubleSidedMap(
            {id_from_coordinates(edge): edge for edge in self._edges},
            recursive_tuple
        )

    def __getattr__(self, item):
        if item == 'edges':
            return [[self.vertices_map[ident] for ident in edge] for edge in self._edges]
        elif item == 'faces':
            return [[self.vertices_map[ident] for ident in face] for face in self._faces]

    def set_edge_data(self, dictionary, key, merge=True):  # todo: make this CombinedDict??
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
        self.edge_data[key] |= translate_dict(dictionary, self.edges_map)

    def get_edge_data(self, key):
        """
        :param key:
        :return: dict with edge (tuple of two tuple-vertices) as keys
        """
        return translate_dict(self.edge_data[key], self.edges_map, recursive_tuple)

    def set_vertex_data(self, dictionary, key, merge=True):  # todo: make this CombinedDict??
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
        self.vertex_data[key] |= translate_dict(dictionary, self.vertices_map)

    def get_vertex_data(self, key):
        """
        :param key:
        :return: dict with edge (tuple of two tuple-vertices) as keys
        """
        return translate_dict(self.vertex_data[key], self.vertices_map, tuple)

    from .mesh_vector_manipulation import replace_vertices
    from .find_entries import find_vertex, find_edges, find_faces


def translate_dict(from_dict, key_key_map, to_key_transformation=return_value):
    to_dict = {}
    for from_key, value in from_dict.items():
        to_key = key_key_map[from_key]
        to_dict[to_key_transformation(to_key)] = value
    return to_dict
