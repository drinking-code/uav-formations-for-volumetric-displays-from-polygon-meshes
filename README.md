# Python Scripts for the UAV Formation Computation Program

This repository contains the Python script(s). For the frontend and the web server,
see [here🔗](https://github.com/drinking-code/uav-formations-interface). Go there to find instructions.

## Prerequisites

- Python 3.11
- perhaps Node.js
- bpy (you have to build yourself, see https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule ; this
  repo assumes that the Python binary is at `blender-git/lib/darwin_arm64/python/bin/python3.10`. THis path may be
  different for you, change it in [`normals/subprocess.py` (line 7)](normals/subprocess.py) if so. bpy is only needed
  for generating normals during the calculation of illumination directionality. As an alternative to building Blender,
  delete `illumination_directionality.py`. The webserver will skip calculating it.)

## Run the script by itself

To look at what the script actually outputs (a bunch of numbers), you can run `run.js`.
Before doing that, create a venv:

```shell
python3.11 -m venv venv
```

install the dependencies (after activating the venv):

```shell
pip install -r requirements.txt
```

and run the file (`node run.js`). It will invoke the python interpreter in the venv to run `main.py` with the contents
of `example_meshes/cube.stl` file as the first argument and example options in JSON format as the second. (If you want to run the script with a different .stl file / options, change [`run.js` at lines 7 and following](run.js).)
