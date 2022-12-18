from functools import reduce

import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import art3d

from utils import recursive_list

color_scale_name = 'plasma'
color_depth = 256
colors = getattr(cm, color_scale_name)(np.linspace(1, 0, color_depth))


def draw_mesh_faces(vectors, axes):
    mesh = art3d.Poly3DCollection(vectors, facecolors='w', zorder=-1)
    axes.add_collection3d(mesh)


def draw_edge_sharpness(sharpness_edges, axes):
    edges = []
    edges_sharpness = []
    for edge, edge_sharpness in sharpness_edges.items():
        edge = recursive_list(edge)
        edges.append(edge)
        edges_sharpness.append(edge_sharpness)
    wire = art3d.Line3DCollection(edges, cmap=color_scale_name)
    wire.set_array(edges_sharpness)
    axes.add_collection(wire)


def draw_corner_sharpness(sharpness_corners, axes):
    i = 1
    for vertex, vertex_sharpness in sharpness_corners.items():
        vertex = list(vertex)
        # if vertex_sharpness < .8:
        #     continue
        color_index = int(np.floor(np.interp(vertex_sharpness, (0, 1), (color_depth - 1, 0))))
        axes.scatter(vertex[0], vertex[1], vertex[2], color=colors[color_index], zorder=20 + i)
        i = i + 1


def center_of_triangle(face):
    def sum_of_nth_values(n, lists):
        return reduce(lambda a, b: a + b, map(lambda list: list[n], lists)) / 3

    return [
        sum_of_nth_values(0, face),
        sum_of_nth_values(1, face),
        sum_of_nth_values(2, face)
    ]


def draw_normals(faces, normals, axes, size=1):
    for face, normal in zip(faces, normals):
        x, y, z = center_of_triangle(face)
        magnitude = np.linalg.norm(normal)
        u, v, w = normal / magnitude * size
        axes.quiver(x, y, z, u, v, w)
