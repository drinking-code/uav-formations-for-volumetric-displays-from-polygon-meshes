from utils import find_in_iterable


def find_vertex(self, is_desired, find_all=False):
    found = {}

    def add_to_found(vertex_tuple):
        vertex_id, vertex = vertex_tuple
        found[vertex_id] = vertex

    find_in_iterable(self.vertices_map, lambda vertex_tuple: is_desired(vertex_tuple[1]), add_to_found, find_all)
    return found


def find_edges(self, is_desired, find_all=False):
    found = {}

    def add_to_found(edge_tuple):
        edge_id, edge = edge_tuple
        found[edge_id] = edge

    find_in_iterable(self.edges_map, lambda edge_tuple: is_desired(edge_tuple[1]), add_to_found, find_all)
    return found
