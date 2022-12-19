def dedupe_verts_in_faces(vertices_map, faces):
    for face in faces:
        for index, vertex in enumerate(face):
            face[index] = vertices_map[vertices_map[vertex]]


def dedupe_verts_in_edges(vertices_map, edges):
    for edge in edges:
        for index, vertex in enumerate(edge):
            edge[index] = vertices_map[vertices_map[vertex]]


def delete_if(iterable, should_be_deleted, delete=None):
    keys_to_delete = []
    for key, value in enumerate(iterable):
        if not should_be_deleted(value):
            continue
        keys_to_delete.append(key)
    keys_to_delete.reverse()
    for key in keys_to_delete:
        if delete is None:
            del iterable[key]
        else:
            delete(key)
    return iterable


def remove_faces_duplicated_vertex(faces):
    """
    Remove faces that have one vertex twice instead of three unique vertices
    :return:
    """
    def face_should_be_deleted(face):
        for index_vertex_a, vertex_a in enumerate(face):
            for vertex_b in face[index_vertex_a + 1:]:
                if vertex_a == vertex_b:
                    return True
        return False

    delete_if(faces, face_should_be_deleted)


def remove_edges_duplicated_vertex(edges, edges_map):
    """
    Remove edges that have one vertex twice instead of two unique vertices
    :return:
    """
    def delete(key):
        del edges_map[edges_map[edges[key]]]
        del edges[key]

    delete_if(edges, lambda edge: edge[0] == edge[1], delete)
