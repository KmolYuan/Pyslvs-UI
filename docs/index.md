# What is Pyslvs?

Pyslvs \[ˈpaɪsɑlvz] is an Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System,
which is named from "Python" and "Solvers".

The project is maintained on GitHub: <https://github.com/KmolYuan/Pyslvs-UI>

See the Windows platform testing on AppVeyor:
[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/Pyslvs-UI)

See the Ubuntu and MacOS platform testing on Travis CI:
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)

!!! note

    Download Pyslvs from GitHub [release page](https://github.com/KmolYuan/Pyslvs-UI/releases),
    which can be executed directly without Python interpreter.
    If you want an open source version, clone it from GitHub.

## How to Startup

Here's some command line options for Pyslvs executable `pyslvs` or `pyslvs.exe`.

```bash
# Open GUI directly
pyslvs

# Open GUI with Fusion style
pyslvs --fusion

# See the help
pyslvs --help
```

Some options for Pyslvs repository.

```bash
# Download / update submodule
git submodule update --init --recursive

# Compile and install submodules
make build-kernel
# Install submodules without --user option
make build-kernel USER_MODE=false

# Open GUI by Python
python launch_pyslvs.py

# Open GUI with Fusion style
python launch_pyslvs.py --fusion

# See the help:
python launch_pyslvs.py --help

# Pack into stand-alone executable file
make
# Without --user option
make USER_MODE=false
```

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

# Using other AppImage options
# https://docs.appimage.org/user-guide/run-appimages.html
./pyslvs.AppImage --appimage-mount
```
