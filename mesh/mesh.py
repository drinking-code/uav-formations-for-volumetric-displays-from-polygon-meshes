from utils.double_sided_dict import DoubleSidedMap
from utils import return_value, recursive_list, recursive_tuple, find_in_iterable, unique_edges as calc_unique_edges, \
    unique_vertices as calc_unique_vertices

from .mesh_vector_manipulation import replace_vertices


class Mesh:
    def __init__(self, data):
        faces = recursive_list(data.vectors)
        self.vertices = calc_unique_vertices(faces)
        self.vertices_map: DoubleSidedMap = DoubleSidedMap(
            {self.id_from_coordinates(vertex): vertex for vertex in self.vertices},
            tuple
        )

        self.faces_refs: list[set] = []
        for face in faces:
            face_ref = set()
            for vertex in face:
                face_ref.add(self.vertices_map[vertex])
            self.faces_refs.append(face_ref)

        self.edges_refs = None
        self.edges_map = None
        self.generate_edges_list()

        self.vertex_data = {}
        self.edge_data = {}

    def generate_edges_list(self):
        self.edges_refs = calc_unique_edges(self.faces_refs)
        self.edges_map: DoubleSidedMap = DoubleSidedMap(
            {self.id_from_coordinates(edge): edge for edge in self.edges_refs},
            recursive_tuple
        )

    def __getattr__(self, item):
        if item == 'edges':
            return [[self.vertices_map[ident] for ident in edge] for edge in self.edges_refs]
        elif item == 'faces':
            return [[self.vertices_map[ident] for ident in face] for face in self.faces_refs]

    def set_edge_data(self, dictionary, key, merge=True):  # todo: make this CombinedDict??
        if merge is False:
            self.edge_data[key].clear()
        if key not in self.edge_data:
            self.edge_data[key] = {}
        self.edge_data[key] |= translate_dict(dictionary, self.edges_map)

    def get_edge_data(self, key):
        return translate_dict(self.edge_data[key], self.edges_map, recursive_tuple)

    def set_vertex_data(self, dictionary, key, merge=True):  # todo: make this CombinedDict??
        if merge is False:
            self.vertex_data[key].clear()
        if key not in self.vertex_data:
            self.vertex_data[key] = {}
        self.vertex_data[key] |= translate_dict(dictionary, self.vertices_map)

    def get_vertex_data(self, key):
        return translate_dict(self.vertex_data[key], self.vertices_map, tuple)

    def replace_vertices(self, vertices_group, target):
        replace_vertices(self, vertices_group, target)

    def find_vertex(self, is_desired, find_all=False):
        return find_x(self.vertices, is_desired, find_all)

    def find_edge(self, is_desired, find_all=False):
        return find_x(self.edges, is_desired, find_all)

    def find_face(self, is_desired, find_all=False):
        return find_x(self.faces, is_desired, find_all)

    def id_from_coordinates(self, coordinates):
        ident = 0
        for index, vertex in enumerate(coordinates):
            ident += (index + 2) ** vertex
        return ident


def translate_dict(from_dict, key_key_map, to_key_transformation=return_value) -> dict:
    to_dict = {}
    for from_key, value in from_dict.items():
        to_key = key_key_map[from_key]
        to_dict[to_key_transformation(to_key)] = value
    return to_dict


def find_x(iterable, is_desired, find_all=False):
    found = []
    find_in_iterable(iterable, is_desired, found.append, find_all)
    return found
