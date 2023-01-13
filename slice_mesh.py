import random

from utils import list_contains


def slice_mesh(mesh, seams):
    slices = {}
    edges_index_of_slice = {}
    face_index = 0
    for face in mesh.faces:
        edges_in_face = []
        for index, vertex_a in enumerate(face):
            for vertex_b in face[index + 1:]:
                edge = mesh.edges_map.find_by_value(
                    lambda edge: list_contains(edge, vertex_a) and list_contains(edge, vertex_b)
                )
                edges_in_face.append(list(edge.values())[0])
        edges_not_seams = list(filter(lambda edge: not list_contains(seams, edge), edges_in_face))
        edges_not_seams = [mesh.edges_map[edge] for edge in edges_not_seams]

        edges_not_seams_slice_indices = []
        for edge_id in edges_not_seams:
            if edge_id in edges_index_of_slice:
                edges_not_seams_slice_indices.append(edges_index_of_slice[edge_id])
        edges_not_seams_slice_indices = list(set(edges_not_seams_slice_indices))
        if len(edges_not_seams_slice_indices) > 1:
            merge_to = edges_not_seams_slice_indices[0]
            for index in edges_not_seams_slice_indices[1:]:
                slices[merge_to] = slices[merge_to] + slices[index]
                del slices[index]
                for edge_id, index_of_slice in edges_index_of_slice.items():
                    if index_of_slice == index_of_slice:
                        edges_index_of_slice[edge_id] = merge_to

        slice_index = edges_not_seams_slice_indices[0] if edges_not_seams_slice_indices else None

        if not slice_index:
            slice_index = random.randint(0, 2 ** 32)
            slices[slice_index] = []
            for edge_id in edges_not_seams:
                edges_index_of_slice[edge_id] = slice_index

        slices[slice_index].append(face)
        face_index += 1
    return slices
