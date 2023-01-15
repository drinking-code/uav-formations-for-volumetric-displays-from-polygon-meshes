import random
from functools import reduce
from pprint import pprint

import numpy as np
from stl import mesh as np_stl
import matplotlib.pyplot as plt

from collapse_vertices import collapse_vertices
from corners_sharpness import calc_corner_sharpness
from distribute_on_edges import distribute_on_edges
from edges_sharpness import calc_edge_sharpness
from mesh import Mesh
from pyplot_draw_mesh import draw_corner_sharpness, draw_edge_sharpness, draw_mesh_faces
from slice_mesh import slice_mesh
from surface_sampling import surface_sampling
from uav_formation import UAVFormation
from unique_vertices import unique_vertices
from utils import triangle_surface_area, recursive_tuple

"""
6. Map colors to points
7. (Optional) perform checks
"""

SHARPNESS_THRESHOLD = .2
MIN_DISTANCE = .1
MAX_AMOUNT_UAV = 300

"""
1. Load data / convert into standardised format
"""
# mesh = mesh.Mesh.from_file('sword.stl')
# mesh = np_stl.Mesh.from_file('sword_double_tip.stl')
# mesh = np_stl.Mesh.from_file('sword_double_tip_ascii.stl')
# mesh = np_stl.Mesh.from_file('monkey.stl')
mesh = np_stl.Mesh.from_file('cube.stl')
mesh = Mesh(mesh)

"""
2. Find hard edges & corners
    - sharpness of corners calculated by taking sum of the angles between all adjacent edges that connect to the vertex.
      deviation of this sum from 360° is the sharpness -> normalised with 0 - 360 => 1 - 0 and 360 - 720 => 0 - 1
"""
sharpness_key = 'sharpness'
mesh.set_vertex_data(calc_corner_sharpness(mesh), sharpness_key)
mesh.set_edge_data(calc_edge_sharpness(mesh), sharpness_key)

"""
3. Reduce hard corners that are too close
"""
collapse_vertices(mesh, SHARPNESS_THRESHOLD, MIN_DISTANCE)

"""
Create formation structure
"""
formation = UAVFormation()

"""
4.1 Distribute points on hard corners (vertices)
"""
sharp_vertices = mesh.find_vertex(
    lambda vertex: mesh.get_vertex_data('sharpness')[tuple(vertex)] > SHARPNESS_THRESHOLD,
    True
)
for vertex_id, vertex in sharp_vertices.items():
    formation[vertex_id][UAVFormation.positions] = vertex
mesh.surface_area = np.sum([triangle_surface_area(face) for face in mesh.faces])

"""
4.2 Distribute points on hard edges _while keeping distance to already generated points_
"""
sharp_edges = mesh.find_edges(
    lambda edge: mesh.get_edge_data('sharpness')[recursive_tuple(edge)] > SHARPNESS_THRESHOLD,
    True
)
density_per_square_unit = MAX_AMOUNT_UAV / mesh.surface_area
density_per_unit = np.sqrt(density_per_square_unit)
wire_vertices = distribute_on_edges(
    list(sharp_edges.values()),
    density_per_unit,
    MIN_DISTANCE,
    list(sharp_vertices.values())
)
for vertex in wire_vertices:
    formation[random.randint(0, 2 ** 32)][UAVFormation.positions] = vertex

"""
5. Distribute points on faces including soft edges and corners (vertices) (bluse noise sampling) _while keeping
   distance to already generated points_
"""
# slice mesh along sharp edges
slices = slice_mesh(mesh, list(sharp_edges.values()))
slices_vectors = [unique_vertices(mesh_slice) for mesh_slice in slices.values()]
# print(slices)
points_on_slices = [surface_sampling(mesh_slice, density_per_square_unit) for mesh_slice in slices.values()]
points_on_slices_flat = reduce(lambda a, b: list(a) + list(b), points_on_slices)
print(len(points_on_slices_flat))

for vertex in points_on_slices_flat:
    formation[random.randint(0, 2 ** 32)][UAVFormation.positions] = vertex

"""
Print stats and show results
"""
total_uav_amount = len(formation)
print(f'UAVs used / UAVs available: {total_uav_amount} / {MAX_AMOUNT_UAV}')
actual_density = total_uav_amount / mesh.surface_area
print(f'Actual density / Aimed density: {np.around(actual_density, 3)} / {np.around(density_per_square_unit, 3)}')

# plot faces and vertices
figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)
axes.set_proj_type('persp', focal_length=0.2)
# axes.set_proj_type('ortho')

colors = ['#FF8686', '#FFD886', '#D6FF86', '#88FF86', '#86FFD7', '#86D7FF', '#8886FF', '#D686FF', '#FF86D8', '#000']
for index, mesh_slice in enumerate(slices.values()):
    draw_mesh_faces(mesh_slice, axes, facecolors=colors[index], opacity=.5)
draw_corner_sharpness({recursive_tuple(vertex): 0 for vertex in formation[UAVFormation.positions].values()}, axes)
draw_edge_sharpness({recursive_tuple(edge): 0 for edge in sharp_edges.values()}, axes)

scale = 2.5
axes.set_xlim3d(scale / -2, scale / 2)
axes.set_ylim3d(scale / -2, scale / 2)
axes.set_zlim3d(0, scale)
axes.set_aspect('equal')
plt.show()
