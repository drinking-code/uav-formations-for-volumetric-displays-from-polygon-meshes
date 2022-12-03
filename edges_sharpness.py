import numpy as np

from angle import angle_between_vectors_anchor
from unique_vertices import unique_edges as calc_unique_edges
from utils import recursive_list, list_contains


def calc_edge_sharpness(faces, normals):
    """
    :param faces: list of faces, each of which is a list containing all its vertices
    :param normals: list of normals for each face
    :returns: dictionary with sharpness value from 0 to 1 for each unique edge given in faces
    """
    faces = recursive_list(faces)
    unique_edges = calc_unique_edges(faces)
    calc_single_edge_sharpness(unique_edges[0], faces, normals)
    sharpness_values = {
        tuple(map(lambda vertex: tuple(vertex), edge)):
            calc_single_edge_sharpness(edge, faces, normals)
        for edge in unique_edges
    }
    return sharpness_values


def calc_single_edge_sharpness(edge, faces, normals):
    faces_with_edge = []
    normals_of_faces_with_edge = []
    for face, normal in (faces, normals):
        matching_vertices = list(filter(lambda vertex: list_contains(edge, vertex), face))
        if len(matching_vertices) == 2:
            faces_with_edge.append(face)
            normals_of_faces_with_edge.append(normal)
    if len(faces_with_edge) > 2:
        raise Exception('More than two faces with the same edge! What the fridge!')

    normal_angle = angle_between_vectors_anchor(faces_with_edge[0], faces_with_edge[1])

    # in case of single flipped angle
    while normal_angle >= 180:
        normal_angle -= 180

    return np.interp(normal_angle, (0, 180), (0, 1))
