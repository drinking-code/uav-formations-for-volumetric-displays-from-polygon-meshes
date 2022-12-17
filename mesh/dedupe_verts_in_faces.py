def dedupe_verts_in_faces(vertices_map, faces):
    for face in faces:
        for index, vertex in enumerate(face):
            face[index] = vertices_map[vertices_map[vertex]]


def dedupe_verts_in_edges(vertices_map, edges):
    for edge in edges:
        for index, vertex in enumerate(edge):
            edge[index] = vertices_map[vertices_map[vertex]]
