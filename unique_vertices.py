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
        for vertex_a in face:
            for vertex_b in face:
                if vertex_a == vertex_b:
                    continue
                edge = [vertex_a, vertex_b]
                is_in_edges = list_contains(edges, edge)
                if is_in_edges:
                    continue
                edges.append(edge)
    return edges
