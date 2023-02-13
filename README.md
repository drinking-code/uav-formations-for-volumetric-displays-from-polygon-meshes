# Python Scripts for the UAV Formation Computation Program

This repository contains the Python script(s). For the frontend and the web server,
see [here🔗](https://github.com/drinking-code/uav-formations-interface). Go there to find instructions.

## Prerequisites

- Python 3.11
- perhaps Node.js

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
of `example_meshes/cube.stl` file as the first argument and example options in JSON format as the second.
