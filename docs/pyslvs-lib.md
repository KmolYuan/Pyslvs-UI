# Pyslvs Libraries

A no-GUI module of mechanism synthesis system and
a 2D geometric constraint solver.

The submodule is located at `pyslvs`.

Pyslvs is now available on
[![PyPI](https://img.shields.io/pypi/v/pyslvs.svg)](https://pypi.org/project/pyslvs/),
you can install it by pip individually:

```bash
pip install pyslvs
```

!!!warning
    Pyslvs-UI is using global `pyslvs` as kernel.
    Please make sure the version is same with it.

## Build and Test

Enter directory and execute the Makefile. Then, run the unit test script after compiling.

```bash
python setup.py test
```

## Module parts

Pyslvs libraries is divided into two following sections:

+ Solver:

    Geometric solver and verification functions.

+ Synthesis:

    Mechanism synthesis system that including several random algorithm and enumeration algorithm, dependent with geometric solver.

Most of classes and functions can be work with a generic Python format (just like a list of coordinates or string-like expression), and you also can cut in at any step.

### Solver

+ **parser** module:

    Analysis expression from strings, turn into symbols object.

+ **expression** library:

    Including PMKS expression object classes.

+ **bfgs** library:

    **preload**: `expression`

    Python wrapper of [Sketch Solve](https://code.google.com/archive/p/sketchsolve/). A simple and fast constraint solver with BFGS algorithm.

+ **tinycadlib** library:

    **preload**: `expression`, `bfgs`

    Particular solution takes more faster then constraint solving.

+ **triangulation** library:

    **preload**: `expression`, `tinycadlib`

    Autometic configuration algorithm for particular solution function in "tinycadlib".

### Kinematic Graph Synthesis

+ **graph** library:

    Graph expression came from NetworkX. Also contains graph verification functions. 

+ **graph_planar** library:

    **preload**: `graph`

    Planar graph checking came from NetworkX.

+ **structural** library:

    **preload**: `graph`, `graph_planar`

    Structural synthesis algorithm.

#### Meta-heuristics Algorithm

[metaheuristics](https://github.com/KmolYuan/metaheuristics) module: Cython algorithms libraries provide evolution designing.

+ **utility** library:

    Provide base fitness function class for algorithm.

+ **rga** library:

    **preload**: `utility`

    Real-coded genetic algorithm for dimensional synthesis.

+ **firefly** library:

    **preload**: `utility`

    Firefly algorithm for dimensional synthesis.

+ **de** library:

    **preload**: `utility`

    Differential Evolution for dimensional synthesis.

#### Dimensional Synthesis

+ **planar_linkage** library:

    **preload**: `expression`, `triangulation`, `bfgs`, `tinycadlib`, `utility`

    Dimensional synthesis verification function objects.
