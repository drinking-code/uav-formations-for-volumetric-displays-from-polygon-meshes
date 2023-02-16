import numpy as np

from utils import list_contains, dihedral_angle


def calc_edge_sharpness(mesh):
    """
    :param mesh: list of faces, each of which is a list containing all its vertices
    :returns: dictionary with sharpness value from 0 to 1 for each unique edge given in faces
    """
    sharpness_values = {
        tuple(edge): calc_single_edge_sharpness(vertices, mesh.find_face)
        for vertices, edge in zip(mesh.edges, mesh.edges_refs)
    }
    return sharpness_values


def calc_single_edge_sharpness(edge, find_faces):
    adjacent_faces = find_faces(lambda face: all(map(lambda vertex: list_contains(face, vertex), edge)), True)

    if len(adjacent_faces) > 2:
        raise Exception('More than two faces with the same edge! What the fridge!')
    # edge only in one face -> consider edge sharp
    elif len(adjacent_faces) < 2:
        return 1

    θ = dihedral_angle(adjacent_faces[0], adjacent_faces[1], edge)
    return np.interp(θ, (0, 180), (1, 0))
