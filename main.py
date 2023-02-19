import json
from sys import argv
import io

import numpy as np
from stl import mesh as np_stl

from sharpness import calc_corner_sharpness, calc_edge_sharpness
from distribute_edges import distribute_on_edges
from mesh import Mesh, slice_mesh, collapse_vertices
from distribute_faces import surface_sampling, is_not_near_points, excluded_area_on_face
from formation import UAVFormation
from utils import triangle_surface_area, find_in_iterable, unique_vertices

stl_contents = argv[1]
options = json.loads(argv[2])

SHARPNESS_THRESHOLD = np.interp(options['sharpness_threshold'], (0, 180), (1, 0))
MIN_DISTANCE = options['min_distance']
MAX_AMOUNT_UAV = options['max_amount']
WIREFRAME_MODE = options['features_only']

"""
1. Load data / convert into standardised format
"""
mesh = np_stl.Mesh.from_file('', fh=io.StringIO(stl_contents))
mesh = Mesh(mesh)

"""
2. Find hard edges & corners
    - sharpness of corners calculated by taking sum of the angles between all adjacent edges that connect to the vertex.
      deviation of this sum from 360° is the sharpness -> normalised with 0 - 360 => 1 - 0 and 360 - 720 => 0 - 1
"""
sharpness_key = 'sharpness'
mesh.set_edge_data(calc_edge_sharpness(mesh), sharpness_key)
mesh.set_vertex_data(calc_corner_sharpness(mesh), sharpness_key)

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
for vertex in sharp_vertices:
    formation.add_position(vertex, UAVFormation.corner)
mesh.surface_area = np.sum([triangle_surface_area(face) for face in mesh.faces])

"""
4.2 Distribute points on hard edges _while keeping distance to already generated points_
"""
sharp_edges = []
find_in_iterable(
    zip(mesh.edges, mesh.edges_refs),
    lambda edge_tuple: mesh.get_edge_data('sharpness')[tuple(edge_tuple[1])] > SHARPNESS_THRESHOLD,
    lambda edge_tuple: sharp_edges.append(edge_tuple[0]),
    True
)
density_per_square_unit = MAX_AMOUNT_UAV / mesh.surface_area
density_per_unit = np.sqrt(density_per_square_unit)
wire_vertices = distribute_on_edges(
    list(sharp_edges),
    density_per_unit,
    MIN_DISTANCE,
    list(sharp_vertices),
    lambda point: formation.add_position(point, UAVFormation.edge)
)

"""
5. Distribute points on faces including soft edges and corners (vertices) (bluse noise sampling) _while keeping
   distance to already generated points_
"""
# slice mesh along sharp edges
slices = slice_mesh(mesh, list(sharp_edges))
slices_vectors = [unique_vertices(mesh_slice) for mesh_slice in slices.values()]
target_distance = max(MIN_DISTANCE, 1 / density_per_square_unit)
sharp_edges_and_corners = formation[UAVFormation.positions].values()
# print(target_distance, MIN_DISTANCE)
# exit(0)
for mesh_slice in slices.values():
    points_on_slice = surface_sampling(
        mesh_slice,
        density_per_square_unit,
        lambda face: excluded_area_on_face(face, sharp_edges_and_corners, target_distance),
        lambda point: is_not_near_points(point, sharp_edges_and_corners, MIN_DISTANCE),
    )
    for point in points_on_slice:
        formation.add_position(point, UAVFormation.face)

"""
7. (Optional) perform checks
"""

# amount_too_close = 0
# distances = []
# for index, point_a in enumerate(formation[UAVFormation.positions].values()):
#     point_distances = []
#     for point_b in list(formation[UAVFormation.positions].values())[index + 1:]:
#         distance = np.linalg.norm(np.subtract(point_b, point_a))
#         point_distances.append(distance)
#         if distance < MIN_DISTANCE:
#             amount_too_close += 1
#     if point_distances:
#         distances.append(min(point_distances))
# maximum_smallest_distance = max(distances)
# avg_distance = np.average(distances)

"""
Print stats and show results
"""
total_uav_amount = len(formation)
# print(f'UAVs used / UAVs available: {total_uav_amount} / {MAX_AMOUNT_UAV}')
# actual_density = total_uav_amount / mesh.surface_area
# print(f'Actual density / Aimed density: {np.around(actual_density, 3)} / {np.around(density_per_square_unit, 3)}')
# print(f'UAVs too close to each other: {amount_too_close}')
# print('Maximum smallest UAV distance / Average smallest UAV distance / MIN_DISTANCE: ' +
#       f'{maximum_smallest_distance} / {avg_distance} / {MIN_DISTANCE}')
