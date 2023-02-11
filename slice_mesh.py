import random
from pprint import pprint

from utils import list_contains


def get_edges_of_face(face, mesh):  # todo: fix: returns None sometimes
    edges_in_face = []
    for index, vertex_a in enumerate(face):
        for vertex_b in face[index + 1:]:
            edge = mesh.find_edges(
                lambda edge: list_contains(edge, vertex_a) and list_contains(edge, vertex_b)
            )
            edges_in_face.append(edge[0])
    return edges_in_face


def slice_mesh(mesh, seams):
    slices = {}
    edges_index_of_slice = {}
    for face in mesh.faces:
        edges_in_face = get_edges_of_face(face, mesh)
        edges_not_seams = list(filter(lambda edge: not list_contains(seams, edge), edges_in_face))
        edges_not_seams = [mesh.edges_map[edge] for edge in edges_not_seams]

        # find adjacent (of placed faces) edges
        edges_not_seams_slice_indices = []
        for edge_id in edges_not_seams:
            if edge_id in edges_index_of_slice:
                edges_not_seams_slice_indices.append(edges_index_of_slice[edge_id])

        # dedupe
        edges_not_seams_slice_indices = list(set(edges_not_seams_slice_indices))

        # merge slices
        if len(edges_not_seams_slice_indices) > 1:
            merge_to = edges_not_seams_slice_indices[0]
            for index in edges_not_seams_slice_indices[1:]:
                # actual merging
                slices[merge_to] = list(slices[merge_to] + slices[index])
                # delete old
                del slices[index]
                # rewrite edge refs
                for edge_id, index_of_slice in edges_index_of_slice.items():
                    if index_of_slice == index:
                        edges_index_of_slice[edge_id] = merge_to

        # set slice index if adjacent edges found
        slice_index = edges_not_seams_slice_indices[0] if edges_not_seams_slice_indices else None

        # create new slice
        if not slice_index:
            slice_index = random.randint(0, 2 ** 32)
            slices[slice_index] = []

        # add face to slice
        slices[slice_index].append(face)
        # add edge refs
        for edge_id in edges_not_seams:
            edges_index_of_slice[edge_id] = slice_index

    return slices
