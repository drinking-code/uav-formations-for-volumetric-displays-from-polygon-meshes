import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from corners_sharpness import calc_corner_sharpness
from edges_sharpness import calc_edge_sharpness
from unique_vertices import unique_vertices
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

mesh = mesh.Mesh.from_file('monkey.stl')

figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)

# find vertices by iterating faces (vertices may appear in more than one face)
vertices = unique_vertices(recursive_list(mesh.vectors))

sharpness_corners = calc_corner_sharpness(mesh.vectors)
sharpness_edges = calc_edge_sharpness(mesh.vectors, mesh.normals)

# plot faces and vertices
# axes.add_collection3d(
#     mplot3d.art3d.Poly3DCollection(mesh.vectors, facecolors='w', lw=1, edgecolor=(0, 0, 0), zorder=-1)
# )
# color_depth = 256
# colors = cm.RdBu(np.linspace(0, 1, color_depth))
# i = 1
# for vertex in vertices:
#     vertex_sharpness = sharpness_corners[tuple(vertex)]
#     if vertex_sharpness < .8:
#         continue
#     color_index = int(np.floor(np.interp(vertex_sharpness, (0, 1), (color_depth - 1, 0))))
#     axes.scatter(vertex[0], vertex[1], vertex[2], color=colors[color_index], zorder=20 + i)
#     i = i + 1
#
# scale = mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)
# plt.show()
