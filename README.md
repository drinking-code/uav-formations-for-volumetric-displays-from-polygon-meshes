# Python Scripts for the UAV Formation Computation Program

This repository contains the Python script(s). For the frontend and the web server,
see [here🔗](https://github.com/drinking-code/uav-formations-interface). Go there to find instructions.

## Prerequisites

- Python 3.11
- perhaps Node.js

## Run the script by itself

To look at what the script actually outputs (a bunch of numbers), you can run `run.js`. Before doing that, obtain an
.stl file (ASCII encoding) containing a simple mesh, for example using Blender
(https://docs.blender.org/manual/en/latest/addons/import_export/mesh_stl.html). Put this file in this directory and line
7 of `run.js` to read

```javascript
const mesh = fs.readFileSync('<your_file.stl>', 'utf-8')
```

If you're at it, you could also play around with the options in the following lines.

Then, create a venv:

```shell
python3.11 -m venv venv
```

install the dependencies (after activating the venv):

```shell
pip install -r requirements.txt
```

and run the file (`node run.js`). It will invoke the python interpreter in the venv to run `main.py` with the contents
of the .stl file as the first argument and the options in JSON format as the second.
