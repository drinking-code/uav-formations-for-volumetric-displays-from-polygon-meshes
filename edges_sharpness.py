import numpy as np

from angle import angle_between_vectors_anchor
from unique_vertices import unique_edges as calc_unique_edges
from utils import recursive_list, list_contains


def calc_edge_sharpness(mesh):
    """
    :param mesh: list of faces, each of which is a list containing all its vertices
    :returns: dictionary with sharpness value from 0 to 1 for each unique edge given in faces
    """
    sharpness_values = {
        tuple(map(lambda vertex: tuple(vertex), edge)):
            calc_single_edge_sharpness(edge, mesh.faces)
        for edge in mesh.edges
    }
    return sharpness_values


def calc_single_edge_sharpness(edge, faces):
    projected_vectors_of_faces_with_edge = []
    a_x, a_y, a_z = edge[0]
    b_x, b_y, b_z = edge[1]
    for face in faces:
        vertices_match = list(map(lambda vertex: list_contains(edge, vertex), face))
        matching_vertices = list(filter(lambda vertex: vertex, vertices_match))
        non_matching_vertex = face[vertices_match.index(False)]
        c_x, c_y, c_z = non_matching_vertex
        if len(matching_vertices) != 2:
            continue

        t = ((c_x - a_x) * (b_x - a_x) + (c_y - a_y) * (b_y - a_y) + (c_z - a_z) * (b_z - a_z)) \
            / \
            ((b_x - a_x) ** 2 + (b_y - a_y) ** 2 + (b_z - a_z) ** 2)
        intersection = [
            a_x + t * (b_x - a_x),
            a_y + t * (b_y - a_y),
            a_z + t * (b_z - a_z),
        ]
        projected_vector = list(np.subtract(non_matching_vertex, intersection))
        projected_vectors_of_faces_with_edge.append(projected_vector)

    if len(projected_vectors_of_faces_with_edge) > 2:
        raise Exception('More than two faces with the same edge! What the fridge!')
    # edge only in one face -> consider edge sharp
    elif len(projected_vectors_of_faces_with_edge) < 2:
        return 1

    θ = angle_between_vectors_anchor(
        projected_vectors_of_faces_with_edge[0],
        projected_vectors_of_faces_with_edge[1]
    )
    return np.interp(θ, (0, 180), (1, 0))
