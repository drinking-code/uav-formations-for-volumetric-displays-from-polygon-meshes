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
    # print(faces)
    for face in faces:
        for index, vertex_a in enumerate(face):
            for vertex_b in face[index:]:
                if vertex_a == vertex_b:
                    continue
                edge = [vertex_a, vertex_b]
                is_in_edges = list_contains(edges, edge) or list_contains(edges, [vertex_b, vertex_a])
                if is_in_edges:
                    continue
                edges.append(edge)
    return edges
