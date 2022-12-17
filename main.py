from stl import mesh as np_stl
import matplotlib.pyplot as plt

from collapse_vertices import collapse_vertices
from corners_sharpness import calc_corner_sharpness
from edges_sharpness import calc_edge_sharpness
from mesh import Mesh
from pyplot_draw_mesh import draw_corner_sharpness, draw_edge_sharpness, draw_mesh_faces, draw_normals
from unique_vertices import unique_vertices, unique_edges
from utils import recursive_list

"""
1. Load data / convert into standardised format
2. Find hard edges & corners
    - sharpness of corners calculated by taking sum of the angles between all adjacent edges that connect to the vertex.
      deviation of this sum from 360° is the sharpness -> normalised with 0 - 360 => 1 - 0 and 360 - 720 => 0 - 1
3. Reduce hard corners that are too close
4. Distribute points on hard corners (vertices)
4. Distribute points on hard edges _while keeping distance to already generated points_
5. Distribute points on faces including soft edges and corners (vertices) (bluse noise sampling) _while keeping
   distance to already generated points_
6. Map colors to points
7. (Optional) perform checks
"""

# mesh = mesh.Mesh.from_file('sword.stl')
mesh = np_stl.Mesh.from_file('sword_double_tip.stl')

figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)
# axes.view_init(elev=10., azim=10)
axes.set_proj_type('persp', focal_length=0.2)

# find vertices by iterating faces (vertices may appear in more than one face)
vectors = mesh.vectors
normals = mesh.normals
mesh = Mesh(mesh)

sharpness_key = 'sharpness'
mesh.set_vertex_data(calc_corner_sharpness(mesh), sharpness_key)
mesh.set_edge_data(calc_edge_sharpness(mesh), sharpness_key)

collapse_vertices(mesh, .1, .1)

# plot faces and vertices
# draw_mesh_faces(mesh.faces, axes)
draw_corner_sharpness(mesh.get_vertex_data(sharpness_key), axes)
draw_edge_sharpness(mesh.get_edge_data(sharpness_key), axes)
# draw_normals(mesh.faces, mesh.normals, axes, .5)

scale = 8
axes.set_xlim3d(scale / -2, scale / 2)
axes.set_ylim3d(scale / -2, scale / 2)
axes.set_zlim3d(0, scale)
plt.show()
