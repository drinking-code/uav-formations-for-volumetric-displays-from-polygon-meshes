from pprint import pprint

import numpy as np
from stl import mesh as np_stl
import matplotlib.pyplot as plt

from collapse_vertices import collapse_vertices
from corners_sharpness import calc_corner_sharpness
from edges_sharpness import calc_edge_sharpness
from mesh import Mesh
from pyplot_draw_mesh import draw_corner_sharpness, draw_edge_sharpness
from uav_formation import UAVFormation
from utils import get_faces_with_vertex_dict, triangle_surface_area

"""
4. Distribute points on hard edges _while keeping distance to already generated points_
5. Distribute points on faces including soft edges and corners (vertices) (bluse noise sampling) _while keeping
   distance to already generated points_
6. Map colors to points
7. (Optional) perform checks
"""

SHARPNESS_THRESHOLD = .1
MIN_DISTANCE = .1
MAX_AMOUNT_UAV = 100

"""
1. Load data / convert into standardised format
"""
# mesh = mesh.Mesh.from_file('sword.stl')
# mesh = np_stl.Mesh.from_file('sword_double_tip.stl')
mesh = np_stl.Mesh.from_file('sword_double_tip_ascii.stl')
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
print(mesh.surface_area)

# plot faces and vertices
figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)
axes.set_proj_type('persp', focal_length=0.2)

draw_corner_sharpness(mesh.get_vertex_data(sharpness_key), axes)
draw_edge_sharpness(mesh.get_edge_data(sharpness_key), axes)

scale = 8
axes.set_xlim3d(scale / -2, scale / 2)
axes.set_ylim3d(scale / -2, scale / 2)
axes.set_zlim3d(0, scale)
# plt.show()
