from utils import list_contains


def unique_vertices(faces):
    vertices = []
    for face in faces:
        for vertex in face:
            is_in_vertices = list_contains(vertices, vertex)
            if is_in_vertices:
                continue
            vertices.append(vertex)

    return vertices


def unique_edges(faces):
    edges = []
    for face in faces:
        face = list(face)
        for index, vertex_a in enumerate(face):
            for vertex_b in face[index + 1:]:
                edge = {vertex_a, vertex_b}
                if not list_contains(edges, edge):
                    edges.append(edge)
    return edges
