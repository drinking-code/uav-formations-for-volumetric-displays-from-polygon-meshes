import json
from sys import argv

import bpy

data = json.loads(argv[1])

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

mesh = bpy.data.meshes.new('imported_mesh')
mesh.from_pydata(data['vertices'], data['edges'], data['faces'])
mesh.update()
obj = bpy.data.objects.new('imported_object', mesh)

collection = bpy.data.collections.new('imported_collection')
bpy.context.scene.collection.children.link(collection)

collection.objects.link(obj)

bpy.context.view_layer.update()

bpy.ops.object.select_all()
# set "obj" explicitly as active object
bpy.context.view_layer.objects.active = obj

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.editmode_toggle()

polygons = obj.data.polygons
# faces = [[vertex for vertex in polygon.vertices] for polygon in obj.data.polygons]
normals = [[coordinate for coordinate in polygon.normal] for polygon in obj.data.polygons]
print('OUTPUT:' + json.dumps(normals))
