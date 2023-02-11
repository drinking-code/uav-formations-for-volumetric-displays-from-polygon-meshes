from utils import find_in_iterable


def find_vertex(self, is_desired, find_all=False):
    found = []
    find_in_iterable(self.vertices, lambda vertex: is_desired(vertex), found.append, find_all)
    return found


def find_edges(self, is_desired, find_all=False):
    found = []
    find_in_iterable(self.edges, lambda edge: is_desired(edge), found.append, find_all)
    return found


def find_faces(self, is_desired, find_all=False):
    found = []
    find_in_iterable(self.faces, lambda face: is_desired(face), found.append, find_all)
    return found
