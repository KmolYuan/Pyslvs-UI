[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/pyslvs-ui)
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)
[![Documentation Status](https://readthedocs.org/projects/pyslvs-ui/badge/?version=latest)](https://pyslvs-ui.readthedocs.io/en/latest/?badge=latest)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/KmolYuan/Pyslvs-UI.svg)](https://github.com/KmolYuan/Pyslvs-UI/releases)
[![Downloads](https://img.shields.io/github/downloads/KmolYuan/Pyslvs-UI/total.svg)](https://github.com/KmolYuan/Pyslvs-UI/releases)

[![PyPI](https://img.shields.io/pypi/v/pyslvs-ui.svg)](https://pypi.org/project/pyslvs-ui/)
[![sourceforge](https://img.shields.io/badge/site-sourceforge-green.svg)](https://sourceforge.net/projects/pyslvs/)
[![kernel](https://img.shields.io/badge/kernel-python--solvespace-orange.svg)](https://github.com/KmolYuan/solvespace)
[![kernel](https://img.shields.io/badge/kernel-pyslvs-orange.svg)](https://github.com/KmolYuan/pyslvs)

# <img width="7%" src="https://github.com/KmolYuan/Pyslvs-UI/raw/master/docs/img/favicon.png" alt="pyslvs-icon"/> Pyslvs-UI

A GUI-based ([PyQt5]) tool used to design 2D linkage mechanism.

+ **Planar Linkages Simulation**
    + Python-Solvespace: Kernel from [Solvespace] with Cython bundle.
    + Pyslvs: Kernel from [Sketch Solve] with Cython.
+ **Mechanical Synthesis**
    + **Number Synthesis**: Combine the attributes of mechanism.
    + **Structural Synthesis**: Cython algorithm used to find out structural possibilities of the mechanism.
    + **Dimensional Synthesis**: Kernel from the three Cython algorithms (rewrite).
+ **Websites**
    + Readthedocs ([stable] / [latest])
    + [Content Management System](http://www.pyslvs.com/content) (to be maintained)
    + [Blog Framework](http://www.pyslvs.com/blog/index.html) (to be maintained)
+ **Others**
    + Cross three platforms.
    + CAD-like user interface.
    + Auto layout of generalized chain.
    + The code complies with [PEP 8] (code format), [PEP 484] (typing) and [PEP 561] (typed package).

If you have any question, please post on GitHub issue or contact <pyslvs@gmail.com>.

[PyQt5]: https://www.riverbankcomputing.com/software/pyqt/download5
[Solvespace]: http://solvespace.com
[Pyslvs]: https://github.com/KmolYuan/pyslvs
[Sketch Solve]: https://code.google.com/archive/p/sketchsolve/
[stable]: https://pyslvs-ui.readthedocs.io/en/stable/
[latest]: https://pyslvs-ui.readthedocs.io/en/latest/
[PEP 8]: https://www.python.org/dev/peps/pep-0008
[PEP 484]: https://www.python.org/dev/peps/pep-0484
[PEP 561]: https://www.python.org/dev/peps/pep-0561

# Getting Started

## Executables

Download portable [executable file](https://github.com/KmolYuan/Pyslvs-UI/releases) of your platform.

## PyPI

```bash
pip install pyslvs-ui
```

## Source

Branch `master` is in development, use `stable` branch to install stable dependencies directly.

```bash
git checkout stable
python setup.py install
```

Or, build `master` branch step by step follow the documentation.

# Documentation

The documentation of Pyslvs and kernel API.
Start it from sources:

```bash
pip install mkdocs
pip install -r doc-requirements.txt
mkdocs serve
```

# Cite

Please see the [reference](https://pyslvs-ui.readthedocs.io/en/stable/references/#cite).
