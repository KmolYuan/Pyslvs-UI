# Python-Solvespace Library

Python wrapper for Solvespace, a geometric constraint solver written in C++.

Python-Solvespace is now available on
[![PyPI](https://img.shields.io/pypi/v/python-solvespace.svg)](https://pypi.org/project/python-solvespace),
you can install it by pip individually:

```bash
pip install python-solvespace
```

!!!warning
    Pyslvs-UI is using global `python-solvespace` as kernel.
    Please make sure the version is meet the requirement.

## Build and Test

Enter directory and execute the Makefile. Then, run the unit test script after compiling.

```bash
make
python tests
```

## Module part

Python-Solvespace has only one library, called "slvs".
