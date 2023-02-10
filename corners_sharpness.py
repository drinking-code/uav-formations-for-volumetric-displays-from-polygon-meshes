from functools import reduce
from pprint import pprint

import numpy as np

from angle import angle_between_vectors_anchor
from unique_vertices import unique_vertices as calc_unique_vertices
from utils import lists_list_filter_contains, recursive_list


def calc_corner_sharpness(mesh):
    """
    :param mesh: list of lists which each contain all vertices forming a face
    :returns: dictionary with sharpness value from 0 to 1 for each unique vertex given in vertices
    """
    sharpness_values = {tuple(vertex): calc_single_corner_sharpness(vertex, mesh.faces) for vertex in mesh.vertices}
    return sharpness_values


def calc_single_corner_sharpness(vertex, faces):
    """
    :param vertex: vertex for which the sharpness shall be returned
    :param faces: list of lists which each contain all vertices forming a face
    :returns: sharpness value from 0 to 1
    """
    connected_vertices = get_connected_vertices(vertex, faces)
    connected_vertices_angles = [
        angle_between_vectors_anchor(connected_vertex[0], connected_vertex[1], vertex)
        for connected_vertex in connected_vertices
    ]
    angles_sum = np.sum(connected_vertices_angles)
    sharpness = np.interp(angles_sum, (0, 360), (1, 0)) \
        if angles_sum <= 360 \
        else np.interp(angles_sum, (360, 360 * 2), (0, 1))
    return sharpness


def get_connected_vertices(vertex, faces):
    """
    :param vertex: vertex for which the connected vertices shall be returned
    :param faces: list of lists which each contain all vertices forming a face
    :returns: list of lists with each two vertices that are adjacent to the given vertex in a face
    """
    faces_with_vertex = lists_list_filter_contains(faces, vertex)
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
