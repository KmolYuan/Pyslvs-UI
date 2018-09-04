[![Version](https://img.shields.io/badge/version-18.09.0-yellow.svg)](https://github.com/KmolYuan/Pyslvs-PyQt5/releases/latest)
[![Build Status](https://img.shields.io/travis/KmolYuan/Pyslvs-PyQt5.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-PyQt5)
[![PyQt](https://img.shields.io/badge/pyqt-5.10%20↑-orange.svg)](https://riverbankcomputing.com/software/pyqt/intro)
[![Downloads](https://img.shields.io/github/downloads/KmolYuan/Pyslvs-PyQt5/total.svg)](https://github.com/KmolYuan/Pyslvs-PyQt5/releases)
[![GitHub license](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://raw.githubusercontent.com/KmolYuan/Pyslvs-PyQt5/master/LICENSE)

![title](icons/Splash.png)

Website: <http://www.pyslvs.com/blog/index.html>

Pyslvs on [Sourceforge](https://sourceforge.net/projects/pyslvs/).

1. [Introduction](#introduction)

    + [Design Method](#design-method)
    + [How to Startup](#how-to-startup)
    + [Symbolic](#symbolic)
    + [Kinematics Simulation](#kinematics-simulation)
    + [Number and Type Synthesis](#number-and-type-synthesis)
    + [Triangular iteration](#triangular-iteration)
    + [Dimensional Synthesis](#dimensional-synthesis)
    + [IO Support](#io-support)

1. [Modules Requirement](#modules-requirement)

    + [Graphviz (Optional)](#graphviz-optional)
    + [PyQt Stuff (Development)](#pyqt-stuff-development)

1. [Kernels Requirement](#kernels-requirement)

    + [Pyslvs Kernel](#pyslvs-kernel)
    + [Python-Solvespace Kernel](#python-solvespace-kernel)

1. [Stand-alone Executable File](#stand-alone-executable-file)

1. [Powered By](#powered-by)

# Introduction

A GUI-based tool use to design 2D linkage mechanism.

+ **Planar Linkages Simulation**:

    - [Python-Solvespace]: Kernel from [Solvespace] with Python bundle (SWIG).
    - [Pyslvs]: Kernel from [Sketch Solve] with Cython.

+ **Mechanical Synthesis**:

    - **Number and Type Synthesis**: Cython algorithm use to find out structure possibilities of the mechanism.
    - **Dimensional Synthesis**: Kernel from three Cython algorithm API (rewrite).

Previews in KDE Plasma desktop:

![main](images/main_plasma.png)

Previews in Windows 10 theme:

![main](images/main_win.png)

## Design Method

![computer_aid_design_method]

Three-steps design flow:

+ Structure Synthesis
+ Dimensional Synthesis
+ Kinematic Simulation

Including sequential processes and inverse analysis.

[computer_aid_design_method]: images/computer_aid_design_method_watermark.png

## How to Startup

Here's some command line options for Pyslvs.

```bash
# Download / update submodule:
git submodule update --init --recursive

# After following compile steps:
make build-kernel

# Open GUI by Python:
python launch_pyslvs.py

# Or see the help:
python launch_pyslvs.py --help

# Run the unit test:
python test_pyslvs.py

# Pack into stand-alone executable file:
make
```

## Symbolic

Referring symbolic from [PMKS](http://designengrlab.github.io/PMKS/).

1. Point

    ![Point](images/Point.png)

1. Link

    ![Link](images/Link.png)

The PMKS expression is using a name label to present a link bar.

A joint between two links will get two name labels, and so on.

The "ground" label is a default name, this link will be the absolute coordinate in the system, might be a frame of your mechanism.

![PMKS example](images/PMKS_example.png)

Pyslvs was translate the PMKS expression as a string, likes below:

```pmks
# Single line annotation.
M[
    J[R, color[Green], P[0.0, 0.0], L[ground, link_0]],
    J[R, color[Green], P[12.92, 32.53], L[link_0, link_1]],
    J[R, color[Green], P[73.28, 67.97], L[link_1, link_2]],
    J[R, color[Green], P[33.3, 66.95], L[link_1]],
    J[R, color[Green], P[90.0, 0.0], L[ground, link_2]],
]
```

Then the expression can be parse in Pyslvs to create the mechanism.

The grammar is defined with Extended Backus–Naur Form (EBNF), you can checkout the source code of parser.

## Kinematics Simulation

Pyslvs has a simple simulation function driving with revolute joints.

![PMKS example](images/Kinemetic.png)

There is a planar constraint solving mechanism done with three CAD kernels:

+ Pyslvs and Sketch Solve.
+ Python-Solvespace.
+ Sketch Solve.

Choose a base point and a driver point for the shaft, then add this dependent into variables list.

Using QDial widget (it just like a turntable) to adjust the angle value of variable.

Path data will start append coordinates (between a certain of distance) after press the "record" button. Press "record" button again to stop recording.

Path data can be copy or switch visibility by right-click menu.

Some exceptions are not support:

+ Other type of joints.
+ Degree of freedom was lower than 1 but still can moving.

## Number and Type Synthesis

Analysis a type of mechanism that exists, and find out other possibilities.

![](images/Number_and_Type_Synthesis.png)

We have a topological algorithm to combine atlas with:

+ Same degree of freedom.
+ Same number of link.
+ Same number of joint.

And use a type of mechanism to do grounding combine.

![](images/Grounding.png)

Grounding combine can merge the structure diagram immediately to canvas.

But in the common ways, you can give it to dimensional synthesis to make it more useful.

## Triangular iteration

Before doing dimensional synthesis, a structure diagram has to configure it's verification formula.

![](images/Triangular_Iteration.png)

**PLAP** function is using two known points, a length variable and an angle variable to find out the position of third point.

**PLLP** function is using two known points and two length variables to find out the position of third point.

When the structure profile is complete, is time to doing dimensional synthesis!

## Dimensional Synthesis

Generate a mechanism with path requirement by random variables.

+ The structure settings is get from triangular iteration.
+ There also have algorithm options, such like constraints or probability.

![](images/Dimensional_Synthesis.png)

Contains three algorithms:

+ Real-coded Genetic Algorithm
+ Firefly Algorithm
+ Differential Evolution

Specify a path and options to generate a crank rocker.

Three kinds of task target:

+ Stop at the maximum generation.
+ Get the minimum fitness value.
+ Stop at the maximum time.

## IO Support

Pyslvs can support for following format.

**Output formats**:

+ Pyslvs workbook database (*.pyslvs).
+ Expression (just a string).
+ [Solvespace] format (*.slvs).
+ DXF format (*.dxf).
+ Image capture (all of [Qt supports]).

[Solvespace]: https://github.com/solvespace/solvespace
[Qt supports]: http://doc.qt.io/qt-5/qimage.html#reading-and-writing-image-files

**Input formats**:

+ Pyslvs workbook database (*.pyslvs).
+ Expression (just a string).
+ Solvespace format (*.slvs, only supports very few of constraints).

The workbook mechanism will generate the sketch frame as \*.slvs format like follow:

![](images/IO_slvs_origin.png)

![](images/IO_slvs_frame.png)

A part file will split the sketch and boundary with two groups.

![](images/IO_slvs_part.png)

The part files can be import to assemble with main sketch file. However, the 3D features still can not be generated from external program yet, so user need to do it by self.

For the IO method of Solvespace format, you can also refer to two Python scripts 'read' and 'write' in Pyslvs IO module.

# Modules Requirement

Actual testing platforms:

+ ![w3.6](https://img.shields.io/badge/Windows%20x64-Python%203.6-blue.svg)
+ ![w3.7](https://img.shields.io/badge/Windows%20x64-Python%203.7-blue.svg) (currently not support PyInstaller)
+ ![u3.6](https://img.shields.io/badge/Ubuntu%20x64-Python%203.6-orange.svg)
+ ![u3.6](https://img.shields.io/badge/Ubuntu%20x64-Python%203.7-orange.svg)

**Please note that the other platforms may be available but I have not tested before.**

**Ubuntu**:

```bash
$ sudo pip3 install -r requirements.txt
```

**Windows**:

Python 3: [Official Python] for Windows 64 bit.

Makefile tool: [MinGW] or [Msys 2][msys].

```bash
> pip install -r requirements.txt
```

## Graphviz (Optional)

Graphviz tools provide some graph engine that can make the position of dots in atlas looks more pretty.

Download it from [here](https://www.graphviz.org/) or:

```bash
$ sudo apt install graphviz
```

Windows user please make sure to add Graphviz `bin` folder path to environment variables.

Then use the `dot` command to check if it works.

If you are not willing to install Graphviz, you can just using built-in layout from NetworkX.

## PyQt Stuff (Development)

PyQt5 and QtChart are now pack into the wheel file that Windows and Ubuntu can install them directly.

Qt tools can use to design the *.ui files, they are not the requirement if you just want to run Pyslvs.

**Ubuntu**:

Download and install [Qt5] to get the tools.

**Windows**:

Windows user can get Qt tools by pip (maybe not newest version), without to install Qt package.

```bash
> pip install pyqt5-tools
```

# Kernels Requirement

About the development tools, please see [Modules Requirement](#modules-requirement).

Make command:

```bash
make build-kernel
```

This project including two kernels should build.

## Pyslvs Kernel

[Pyslvs]\: Core libraries of this project.

Make command:

```bash
make build-pyslvs
```

**Ubuntu**:

Ubuntu user can compile the kernel by Cython directly.

**Windows**:

There's two options to choose SDK:

1. Using Microsoft Visual Studio. You can get it from [here][visualstudio-link], then startup the Visual Studio Community and install Windows SDK.
1. Using [Msys 2][msys]. It is based on MinGW 64-bit version.
1. Just using [MinGW 64-bit][mingw64].

[visualstudio-link]: https://www.visualstudio.com/downloads/
[msys]: http://www.msys2.org/
[mingw64]: https://sourceforge.net/projects/mingw-w64/

When using MinGW, you can refer the steps of this article: <https://stackoverflow.com/questions/34135280/valueerror-unknown-ms-compiler-version-1900>

## Python-Solvespace Kernel

[Python-Solvespace]\: Python boundle of [Solvespace] library.

Make command:

```bash
make build-solvespace
```

**Ubuntu**:

Install SWIG and Python development kit. This tool kit can make a Python bundle with C/C++ library.

```bash
sudo apt install swig python3-dev
```

**Windows**:

Download and install [SWIG](http://www.swig.org/download.html).

# Stand-alone Executable File

As your wish, it can be renamed or moved out and operate independently in no-Python environment.

**Ubuntu**:

Use shell command to build as [AppImage](https://github.com/AppImage/AppImages).

After following operation, the executable file is in `out` folder.

Make command:

```bash
$ sudo pip3 install virtualenv
$ make
```

**Windows**:

Use PyInstaller to build.

After following operation, the executable file is in `dist` folder.

Make command:

```bash
> pip install pyinstaller
> make
```

# Powered By

Made by [Qt5] and Python IDE [Eric 6].

If there is no special reason, please install the new version of the kits.

Including Python modules:

* [SIP] (GPLv2, GPLv3)
* [PyQt5], [PyQtChart] (GPLv3)
* [ezdxf] (MIT)
* [numpy] (BSD 3-Clause)
* [Cython] (Apache 2.0)
* [openpyxl] (MIT)
* [psutil] (BSD)
* [peewee] (MIT)
* [Lark-parser] (MIT)
* [NetworkX] (BSD 3-Clause)
* [Pydot] (MIT)
* [Pygments] (BSD)

Pyslvs is under [GNU Affero General Public License v3].

Kernel repository:

* [Pyslvs]
* [Python-solvespace]

[Solvespace]: http://solvespace.com
[PyQt5]: https://www.riverbankcomputing.com/software/pyqt/download5
[PyQtChart]: https://www.riverbankcomputing.com/software/pyqtchart/download
[Qt5]: https://www.qt.io/download/
[SIP]: https://riverbankcomputing.com/software/sip/download

[Official Python]: https://www.python.org/
[MinGW]: https://sourceforge.net/projects/mingw-w64/files/

[Eric 6]: http://eric-ide.python-projects.org/

[numpy]: http://www.numpy.org/
[ezdxf]: https://ezdxf.readthedocs.io/en/latest/index.html
[Cython]: http://cython.org/
[openpyxl]: http://openpyxl.readthedocs.io/
[psutil]: https://github.com/giampaolo/psutil
[peewee]: http://docs.peewee-orm.com/en/latest/
[Lark-parser]: https://github.com/erezsh/lark
[NetworkX]: https://networkx.github.io/
[Pydot]: https://github.com/erocarrera/pydot
[Pygments]: http://pygments.org/

[Python-Solvespace]: https://github.com/KmolYuan/python-solvespace
[Pyslvs]: https://github.com/KmolYuan/pyslvs
[Sketch Solve]: https://code.google.com/archive/p/sketchsolve/

[GNU Affero General Public License v3]: https://github.com/KmolYuan/Pyslvs-PyQt5/blob/master/LICENSE
