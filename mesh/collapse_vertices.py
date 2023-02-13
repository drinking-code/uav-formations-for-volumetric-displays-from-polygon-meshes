import numpy as np

from utils import recursive_list, list_contains


def collapse_vertices(mesh, sharpness_threshold, minimum_distance):
    faces_with_vertex = get_faces_with_vertex_dict(mesh.faces)
    # filter out non-sharp vertices
    faces_with_vertex = {
        vertex: face
        for vertex, face in faces_with_vertex.items()
        if mesh.get_vertex_data('sharpness')[vertex] > sharpness_threshold
    }

    # find the middle (average) for each group
    # collapse group into middle

    # what about larger clusters where the two farthest points are farther away than threshold
    # -> unlikely to exist because clusters are filtered by sharpness

    sharp_vertices = recursive_list(faces_with_vertex.keys())
    collapsed_vertices = []
    for index, vertex_subject in enumerate(sharp_vertices):
        if list_contains(collapsed_vertices, vertex_subject):
            continue
        vertex_group = [vertex_subject]
        for vertex_to_compare in sharp_vertices[index:]:
            if list_contains(collapsed_vertices, vertex_to_compare):
                continue
            if vertex_subject == vertex_to_compare:
                continue
            distance = np.linalg.norm(np.subtract(vertex_to_compare, vertex_subject))
            if distance >= minimum_distance:
                continue
            vertex_group.append(vertex_to_compare)

        # vertex_subject will only be moved if other vertices that are too close are found
        if len(vertex_group) > 1:
            collapsed_vertices.extend(vertex_group)
            middle_point = np.average(vertex_group, axis=0)
            mesh.replace_vertices(vertex_group, middle_point)


def get_faces_with_vertex_dict(mesh):
    """
    Returns a dictionary with all occurring vertices as keys and a list of faces that include a vertex as values
    :param mesh:
    :return:
    """
    faces_with_vertex = {}
    for face in mesh:
        for vertex in face:
            vertex = tuple(vertex)
            if vertex not in faces_with_vertex:
                faces_with_vertex[vertex] = []
            faces_with_vertex[vertex].append(face)
    return faces_with_vertex
