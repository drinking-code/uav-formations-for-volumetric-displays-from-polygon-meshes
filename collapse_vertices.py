import numpy as np

from utils import get_faces_with_vertex_dict, recursive_list


def collapse_vertices(vertices_sharpness, mesh, sharpness_threshold, minimum_distance, axes):
    faces_with_vertex = get_faces_with_vertex_dict(mesh)
    # filter out non-sharp vertices
    faces_with_vertex = {
        vertex: face
        for vertex, face in faces_with_vertex.items()
        if vertices_sharpness[vertex] > sharpness_threshold
    }

    # find "groups" of close vertices
    # find the middle (average) for each group
    # collapse group into middle

    # what about larger clusters where the two farthest points are farther away than threshold
    # -> unlikely to exist because clusters are filtered by sharpness

    sharp_vertices = faces_with_vertex.keys()
    for vertex_subject in sharp_vertices:
        for vertex_to_compare in sharp_vertices:
            if vertex_subject == vertex_to_compare:
                continue
            distance = np.linalg.norm(np.subtract(vertex_to_compare, vertex_subject))
            if distance >= minimum_distance:
                continue

            middle_point = np.average([list(vertex_to_compare), list(vertex_subject)], axis=0)
            axes.scatter(middle_point[0], middle_point[1], middle_point[2], color='black', zorder=20)
