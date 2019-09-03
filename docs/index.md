# What is Pyslvs?

Pyslvs \[`paɪsɑlvz] is an Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System,
which is named from "Python" and "Solvers".

The project is maintained on GitHub: <https://github.com/KmolYuan/Pyslvs-UI>

See the Windows platform testing on AppVeyor:
[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/pyslvs-pyqt5)

See the Ubuntu and macOS platform testing on Travis CI:
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)

## How to Startup

Download Pyslvs from GitHub [release page](https://github.com/KmolYuan/Pyslvs-UI/releases),
which can be executed directly without Python interpreter.
If you want an open source version, clone it from GitHub.

### Windows and MacOS Platform

Here's some command line options for Pyslvs executable.

For convenience, the file name of distributions can rename as `pyslvs.exe`, `pyslvs.app` or `pyslvs.AppImage`,
the suffix is depended on your platform.

```bash
# Open GUI directly
pyslvs

# Open GUI with Fusion style
pyslvs --fusion

# See the help
pyslvs --help
```

### Ubuntu Platform

Python libraries has some dependencies with the compile environment,
so the sources need to packed the Python installation and its libraries.
But the source code is presented as plain text, which causes
the size of AppImage is larger than other platforms.

Here's some options for AppImage release `pyslvs.AppImage` for Ubuntu platform.

```bash
# Run it as a normal executable
chomod +x pyslvs.AppImage
./pyslvs.AppImage

# Unzip the package to "squashfs-root"
# There is including the source code of Pyslvs
./pyslvs.AppImage --appimage-extract
```

You can refer other AppImage options from its [user guide](https://docs.appimage.org/user-guide/run-appimages.html).

### Git Repository

Some options for Pyslvs repository.

For more environment information, please see [Environment section](environment.md).

!!! warning

    Pyslvs requires Python 3.7 or above.

```bash
# Download / update submodule
git submodule update --init --recursive

# Install dependencies
pip install -r requirements.txt

# Compile and install submodules
make build-kernel

# Open GUI by Python
python launch_pyslvs.py

# Pack into stand-alone executable file
make
```
