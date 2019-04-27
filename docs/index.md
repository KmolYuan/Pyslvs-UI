# Pyslvs Manual

Pyslvs is an Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System.

The project is maintained on GitHub: <https://github.com/KmolYuan/Pyslvs-UI>

See the Windows platform testing on AppVeyor:
[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/pyslvs-pyqt5)

See the Ubuntu and MacOS platform testing on Travis CI:
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)

!!! Note

    Download Pyslvs from GitHub [release page](https://github.com/KmolYuan/Pyslvs-UI/releases),
    which can be executed directly without Python interpreter.
    If you want an open source version, clone it from GitHub.

## How to Startup

Here's some command line options for Pyslvs executable file.

```bash
# Open GUI directly:
pyslvs

# Open GUI with Fusion style:
pyslvs --fusion

# See the help:
pyslvs --help
```

Here's some command line options for Pyslvs repository.

```bash
# Download / update submodule:
git submodule update --init --recursive

# After following compile steps:
make build-kernel

# Open GUI by Python:
python launch_pyslvs.py

# Open GUI with Fusion style:
python launch_pyslvs.py --fusion

# See the help:
python launch_pyslvs.py --help

# Pack into stand-alone executable file:
make
```
