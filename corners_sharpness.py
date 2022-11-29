from functools import reduce

import numpy as np

from unique_vertices import unique_vertices as calc_unique_vertices
from utils import lists_list_filter_contains, recursive_list


def calc_corner_sharpness(vertices):
    """
    :param vertices: list of lists which each contain all vertices forming a face
    :returns: dictionary with sharpness value from 0 to 1 for each unique vertex given in vertices
    """
    vertices = recursive_list(vertices)
    unique_vertices = calc_unique_vertices(vertices)
    sharpness_values = {tuple(vertex): calc_single_corner_sharpness(vertex, vertices) for vertex in unique_vertices}
    return sharpness_values


def calc_single_corner_sharpness(vertex, vertices):
    """
    :param vertex: vertex for which the sharpness shall be returned
    :param vertices: list of lists which each contain all vertices forming a face
    :returns: sharpness value from 0 to 1
    """
    vertex = list(vertex)
    connected_vertices = get_connected_vertices(vertex, vertices)
    connected_vertices_angles = [
        angle_between_vectors_anchor(connected_vertex[0], connected_vertex[1], vertex)
        for connected_vertex in connected_vertices
    ]
    angles_sum = reduce(lambda a, b: a + b, connected_vertices_angles)
    sharpness = np.interp(angles_sum, (0, 360), (1, 0)) \
        if angles_sum <= 360 \
        else np.interp(angles_sum, (360, 360 * 2), (0, 1))
    return sharpness


def get_connected_vertices(vertex, vertices):
    """
    :param vertex: vertex for which the connected vertices shall be returned
    :param vertices: list of lists which each contain all vertices forming a face
    :returns: list of lists with each two vertices that are adjacent to the given vertex in a face
    """
    faces_with_vertex = lists_list_filter_contains(vertices, vertex)
    # copy faces
    faces_with_vertex = recursive_list(faces_with_vertex)
    for face in faces_with_vertex:
        # remove given vertex
        del face[face.index(vertex)]
        if len(face) == 2:
            continue
        else:
            raise Exception('Implement filtering only two connected vertices')

    return faces_with_vertex


def angle_between_vectors_anchor(vector_u, vector_v, vector_anchor=None):
    """
    Calculates the angle between vector_u and vector_v, taking vector_anchor as the origin
    :returns: angle θ
    """
    if vector_anchor is None:
        vector_anchor = [0, 0, 0]
    vector_u, vector_v, vector_anchor = np.array(vector_u), np.array(vector_v), np.array(vector_anchor)
    vector_u = vector_u - vector_anchor
    vector_v = vector_v - vector_anchor
    cos_θ = np.dot(vector_u, vector_v) / (np.linalg.norm(vector_u) * np.linalg.norm(vector_v))
    θ_rad = np.arccos(cos_θ)
    θ = np.degrees(θ_rad)
    while θ > 90:
        θ = θ - 90
    return θ
