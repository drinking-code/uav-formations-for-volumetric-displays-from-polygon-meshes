from utils import list_contains


def unique_vertices(faces):
    vertices = []
    for face in faces:
        for vertex in face:
            is_vertex_list = list_contains(vertices, list(vertex), list)
            is_in_vertices = any(is_vertex_list)
            if is_in_vertices:
                continue
            vertices.append(vertex)

    return vertices
