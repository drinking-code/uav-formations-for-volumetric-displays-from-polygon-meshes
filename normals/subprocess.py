import json
import subprocess
from os.path import isfile

from utils import unique_vertices, unique_edges

blenderPythonBin = 'blender-git/lib/darwin_arm64/python/bin/python3.10'
if not isfile(blenderPythonBin):
    print('Could not find bpy module, please build it first.')
    exit(1)


def run_normals_make_consistent_37(faces):
    edges = unique_edges(faces, True)
    vertices = unique_vertices(faces)
    faces = [[vertices.index(vertex) for vertex in face] for face in faces]
    edges = [[vertices.index(vertex) for vertex in edge] for edge in edges]
    vertices = [[float(coordinate) for coordinate in vertex] for vertex in vertices]
    faces_json = json.dumps({
        'faces': faces,
        'edges': edges,
        'vertices': vertices,
    })
    # returns normals in the order that the faces were given
    output = subprocess.run([blenderPythonBin, 'normals/normals_make_consistent.py', faces_json], capture_output=True)

    for line in output.stdout.splitlines():
        line = line.decode('utf-8')
        if not line.startswith('OUTPUT:'):
            continue
        line = line.replace('OUTPUT:', '')
        return json.loads(line)
