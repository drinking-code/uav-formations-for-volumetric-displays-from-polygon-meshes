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
from surface_sampling.points_on_surface_utils import area_of_radii_on_surface, is_not_near_points
from uav_formation import UAVFormation
from unique_vertices import unique_vertices
from utils import triangle_surface_area, recursive_tuple

"""
todo
6. Map colors to points
"""

SHARPNESS_THRESHOLD = .2
MIN_DISTANCE = .1
MAX_AMOUNT_UAV = 500

"""
1. Load data / convert into standardised format
"""
# mesh = np_stl.Mesh.from_file('sword.stl')
mesh = np_stl.Mesh.from_file('icosphere.stl')
# mesh = np_stl.Mesh.from_file('sword_double_tip.stl')
# mesh = np_stl.Mesh.from_file('sword_double_tip_ascii.stl')
# mesh = np_stl.Mesh.from_file('monkey.stl')
# mesh = np_stl.Mesh.from_file('cube.stl')
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
# print(MIN_DISTANCE, 1 / density_per_square_unit)
target_distance = max(MIN_DISTANCE, 1 / density_per_square_unit)
points_on_slices = [
    surface_sampling(
        mesh_slice,
        density_per_square_unit,
        lambda point: is_not_near_points(point, list(sharp_vertices.values()) + list(wire_vertices), target_distance),
        area_of_radii_on_surface(list(sharp_vertices.values()), wire_vertices, target_distance, mesh_slice)
    )
    for mesh_slice in slices.values()
]
points_on_slices_flat = reduce(lambda a, b: list(a) + list(b), points_on_slices)

for vertex in points_on_slices_flat:
    formation[random.randint(0, 2 ** 32)][UAVFormation.positions] = vertex

"""
7. (Optional) perform checks
"""

amount_too_close = 0
distances = []
for index, point_a in enumerate(formation[UAVFormation.positions].values()):
    point_distances = []
    for point_b in list(formation[UAVFormation.positions].values())[index + 1:]:
        distance = np.linalg.norm(np.subtract(point_b, point_a))
        point_distances.append(distance)
        if distance < MIN_DISTANCE:
            amount_too_close += 1
    if point_distances:
        distances.append(min(point_distances))
avg_distance = np.average(distances)

"""
Print stats and show results
"""
total_uav_amount = len(formation)
print(f'UAVs used / UAVs available: {total_uav_amount} / {MAX_AMOUNT_UAV}')
actual_density = total_uav_amount / mesh.surface_area
print(f'Actual density / Aimed density: {np.around(actual_density, 3)} / {np.around(density_per_square_unit, 3)}')
print()
print(f'UAVs too close to each other: {amount_too_close}')
print(f'Average smallest UAV distance / MIN_DISTANCE: {avg_distance} / {MIN_DISTANCE}')

# plot faces and vertices
figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)
axes.set_proj_type('persp', focal_length=0.2)
# axes.set_proj_type('ortho')

colors = ['#FF8686', '#FFD886', '#D6FF86', '#88FF86', '#86FFD7', '#86D7FF', '#8886FF', '#D686FF', '#FF86D8', '#000']
# for index, mesh_slice in enumerate(slices.values()):
#     draw_mesh_faces(mesh_slice, axes, facecolors=colors[index], opacity=.5)

# draw_corner_sharpness({recursive_tuple(vertex): int(
#     not is_not_near_points(vertex, list(sharp_vertices.values()) + list(wire_vertices), MIN_DISTANCE)) for vertex in
#                        points_on_slices_flat}, axes)
draw_corner_sharpness({recursive_tuple(vertex): 0 for vertex in formation[UAVFormation.positions].values()}, axes)
# draw_edge_sharpness({recursive_tuple(edge): 0 for edge in sharp_edges.values()}, axes)

scale = target_distance
# u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
# x = np.cos(u) * np.sin(v) * scale
# y = np.sin(u) * np.sin(v) * scale
# z = np.cos(v) * scale
# axes.plot_wireframe(x, y, z, color="r")

scale = 2
axes.set_xlim3d(scale / -2, scale / 2)
axes.set_ylim3d(scale / -2, scale / 2)
axes.set_zlim3d(0, scale)
axes.set_aspect('equal')
plt.show()
