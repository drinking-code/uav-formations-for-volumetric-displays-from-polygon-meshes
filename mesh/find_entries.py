from utils import find_in_iterable


def find_x(iterable, is_desired, find_all=False):
    found = []
    find_in_iterable(iterable, is_desired, found.append, find_all)
    return found


def find_vertex(self, is_desired, find_all=False):
    return find_x(self.vertices, is_desired, find_all)


def find_edges(self, is_desired, find_all=False):
    return find_x(self.edges, is_desired, find_all)


def find_edges_refs(self, is_desired, find_all=False):
    return find_x(self._edges, is_desired, find_all)


def find_faces(self, is_desired, find_all=False):
    return find_x(self.faces, is_desired, find_all)
