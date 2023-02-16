import numpy as np

from .algebra import angle_between_vectors_anchor

from .iterables import find_in_iterable, list_contains


def face_spine_edge_to_vertex(edge, vertex):
    a_x, a_y, a_z = edge[0]
    b_x, b_y, b_z = edge[1]
    c_x, c_y, c_z = vertex

    t = ((c_x - a_x) * (b_x - a_x) + (c_y - a_y) * (b_y - a_y) + (c_z - a_z) * (b_z - a_z)) / \
        ((b_x - a_x) ** 2 + (b_y - a_y) ** 2 + (b_z - a_z) ** 2)
    intersection = [
        a_x + t * (b_x - a_x),
        a_y + t * (b_y - a_y),
        a_z + t * (b_z - a_z),
    ]

    return list(np.subtract(vertex, intersection))


def dihedral_angle(face_a, face_b, common_edge=None):
    θ, spines = dihedral_angle_and_spines(face_a, face_b, common_edge)
    return θ


def dihedral_angle_and_spines(face_a, face_b, common_edge=None):
    if not common_edge:
        common_edge = list(filter(lambda vertex: list_contains(face_b, vertex), face_a))

    def find_spine(face):
        non_matching_vertex = []
        find_in_iterable(face, lambda vertex: not list_contains(common_edge, vertex), non_matching_vertex.append)
        return face_spine_edge_to_vertex(common_edge, non_matching_vertex[0])

    spines = [find_spine(face) for face in (face_a, face_b)]

    θ = angle_between_vectors_anchor(spines[0], spines[1])

    return θ, spines
