def dedupe_verts_in_faces(vertices_map, faces):
    for face in faces:
        for index, vertex in enumerate(face):
            face[index] = vertices_map[vertices_map[vertex]]


def dedupe_verts_in_edges(vertices_map, edges):
    for edge in edges:
        for index, vertex in enumerate(edge):
            edge[index] = vertices_map[vertices_map[vertex]]


def remove_faces_duplicated_vertex(faces):
    """
    Remove faces that have one vertex twice instead of the unique vertices
    :return:
    """
    faces_indices_to_delete = []
    for index_face, face in enumerate(faces):
        for index_vertex_a, vertex_a in enumerate(face):
            do_break = False
            for vertex_b in face[index_vertex_a + 1:]:
                if vertex_a != vertex_b:
                    continue
                do_break = True
                faces_indices_to_delete.append(index_face)
                break
            if do_break:
                break
    faces_indices_to_delete.reverse()
    for index_face in faces_indices_to_delete:
        del faces[index_face]
