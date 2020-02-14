# What is Pyslvs?

<img width="7%" src="https://github.com/KmolYuan/Pyslvs-UI/raw/master/docs/img/favicon.png" alt="pyslvs-icon"/>
Pyslvs \[`paɪsɑlvz] is an
**open source planar linkage mechanism simulation and mechanical synthesis system**,
which is named from "Python" and "Solvers".

The project is maintained on GitHub: <https://github.com/KmolYuan/Pyslvs-UI>

See the Windows platform testing on AppVeyor:
[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/pyslvs-ui)

See the Ubuntu and macOS platform testing on Travis CI:
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)

## Install

!!! note
    Feel free to uninstall Pyslvs by [uninstall guide](#uninstall).

!!! warning
    Pyslvs requires Python 3.7 or above.

### PyPI

Pyslvs-UI from PyPI:
[![PyPI](https://img.shields.io/pypi/v/pyslvs-ui.svg)](https://pypi.org/project/pyslvs-ui)

Pyslvs from PyPI:
[![PyPI](https://img.shields.io/pypi/v/pyslvs.svg)](https://pypi.org/project/pyslvs)

Python-Solvespace from PyPI:
[![PyPI](https://img.shields.io/pypi/v/python-solvespace.svg)](https://pypi.org/project/python-solvespace)

```bash
pip install pyslvs-ui
```

!!! note
    Pyslvs-UI is an universal (pure Python) package, which is cross-platform.

    But the core kernel is installed from PyPI,
    Windows and macOS platform are packed as wheels,
    Linux platform will build from source code.

### Portable

Download Pyslvs from GitHub [release page](https://github.com/KmolYuan/Pyslvs-UI/releases),
which can be executed directly without Python interpreter.

I hope your platform is supported, if not,
please try another way or help me improve my Continuous Deployment process.

### Run Directly

Recommended for developers.
If you want an open source version,
please clone it from GitHub then follow the develop environment [guide](environment.md)
and [execute the launcher](#repository).

Or, install it with setuptools. The kernels will installed by pip.
(Only for stable version!)

```bash
python setup.py install
```

## Startup

### Python Package and Executable

After installed package, Pyslvs provides a launcher command `pyslvs` for your terminal.
The command `python -m pyslvs_ui` or write a python script also works:

```python
from pyslvs_ui.__main__ import main
main()
```

For convenience, the file name of distributions can be renamed as
`pyslvs.exe`, `pyslvs.app` or `pyslvs.AppImage`,
the suffix is depended on your platform.

Here's some command line options for Pyslvs executable.

```bash
# Open GUI directly
pyslvs

# Open GUI with Fusion style
pyslvs --fusion

# See the help
pyslvs --help
```

### AppImage

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

### Repository

Some options for Pyslvs repository.

For more environment information, please see [Environment section](environment.md).

```bash
# Download / update submodule
git submodule update --init --recursive

# Install dependencies
pip install -r requirements.txt

# Compile and install submodules
make

# Open GUI by Python
python launch_pyslvs.py

# Pack into stand-alone executable file
make pack
```

## Uninstall

For PyPI package, uninstall Pyslvs-UI and its kernels by `pip`.

```bash
pip uninstall pyslvs-ui pyslvs python-solvespace
```

For other distributions, just delete the file or repository.
