import numpy as np
from stl import mesh as np_stl, stl
from icosphere import icosphere

from uav_formation import UAVFormation


def save_as_stl(formation, diameter):
    all_vertices = []
    all_faces = []
    for point in formation[UAVFormation.positions].values():
        vertices, faces = sphere(point, diameter)
        all_vertices_len = len(all_vertices)
        faces = [[[vertex_id + all_vertices_len] for vertex_id in face] for face in faces]
        all_vertices += list(vertices)
        all_faces += list(faces)

    all_vertices = np.array(all_vertices)
    all_faces = np.array(all_faces)
    mesh = np_stl.Mesh(np.zeros(all_faces.shape[0], dtype=np_stl.Mesh.dtype))
    for i, face in enumerate(all_faces):
        for j in range(3):
            mesh.vectors[i][j] = all_vertices[face[j], :]
    mesh.save('out.stl', mode=stl.ASCII)


def sphere(position, scale):
    vertices, faces = icosphere(2)
    # faces = vertices[faces]
    vertices = [[
        coordinate * scale + offset
        for coordinate, offset in zip(vertex, position)
    ] for vertex in vertices]
    return vertices, faces
