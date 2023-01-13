from pprint import pprint

from double_sided_dict import DoubleSidedMap
from utils import list_contains


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
        if not (
                should_be_deleted(value, key)
                if should_be_deleted.__code__.co_argcount == 2
                else should_be_deleted(value)
        ):
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


def remove_edges_duplicated_vertex(edges, edges_map: DoubleSidedMap):
    """
    Remove edges that have one vertex twice instead of two unique vertices
    :return:
    """

    def delete(key):
        for edge_key in edges_map.get_all(edges[key]):
            del edges_map[edge_key]
        del edges[key]

    delete_if(edges, lambda edge: edge[0] == edge[1], delete)


def gracefully_dedupe_edges(edges, edges_map):
    """
    Remove edges appear more than once in the array, for example once `[v_a, v_b]` and another time as `[v_b, v_a]`.
    Keeps the key of the duplicated edge in edges_map but points it to the original edge.
    :return:
    """
    seen_edges = []
    should_be_deleted_keys = {}

    def should_be_deleted(edge, index):
        edge_reverse = edge.copy()
        edge_reverse.reverse()
        was_seen = False
        index_of_seen = -1
        if list_contains(seen_edges, edge):
            was_seen = True
            index_of_seen = seen_edges.index(edge)
        elif list_contains(seen_edges, edge_reverse):
            was_seen = True
            index_of_seen = seen_edges.index(edge_reverse)
        seen_edges.append(edge)
        should_be_deleted_keys[index] = edges_map[seen_edges[index_of_seen]]
        return was_seen

    def delete(key):
        key_from = edges_map[edges[key]]
        key_to = should_be_deleted_keys[key]
        if key_from != key_to:
            edges_map.point_key_to(edges_map[edges[key]], should_be_deleted_keys[key])
        del edges[key]

    delete_if(edges, should_be_deleted, delete)
