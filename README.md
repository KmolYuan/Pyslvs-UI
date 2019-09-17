[![Version](https://img.shields.io/badge/version-19.09.0-yellow.svg)](https://github.com/KmolYuan/Pyslvs-UI/releases/latest)
[![Build status](https://ci.appveyor.com/api/projects/status/d2rxv6psmuj5fco9?svg=true)](https://ci.appveyor.com/project/KmolYuan/pyslvs-pyqt5)
[![Build status](https://img.shields.io/travis/KmolYuan/Pyslvs-UI.svg?logo=travis)](https://travis-ci.org/KmolYuan/Pyslvs-UI)
[![Documentation Status](https://readthedocs.org/projects/pyslvs-ui/badge/?version=latest)](https://pyslvs-ui.readthedocs.io/en/latest/?badge=latest)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/KmolYuan/Pyslvs-UI.svg)](https://github.com/KmolYuan/Pyslvs-UI/releases)
[![Downloads](https://img.shields.io/github/downloads/KmolYuan/Pyslvs-UI/total.svg)](https://github.com/KmolYuan/Pyslvs-UI/releases)

[![kernel](https://img.shields.io/badge/kernel-python%20solvespace-orange.svg)](https://github.com/KmolYuan/solvespace)
[![kernel](https://img.shields.io/badge/kernel-pyslvs-orange.svg)](https://github.com/KmolYuan/pyslvs)
[![PyPI](https://img.shields.io/pypi/v/pyslvs-ui.svg)](https://pypi.org/project/pyslvs-ui/)
[![sourceforge](https://img.shields.io/badge/site-sourceforge-green.svg)](https://sourceforge.net/projects/pyslvs/)
[![Blog](https://img.shields.io/badge/info-blog-blue.svg)](http://www.pyslvs.com/blog/index.html)
[![CMS](https://img.shields.io/badge/info-cms-blue.svg)](http://www.pyslvs.com/content/)

![title](icons/splash.png)

# Introduction

A GUI-based ([PyQt5]) tool used to design 2D linkage mechanism.

+ **Planar Linkages Simulation**

    - [Python-Solvespace]: Kernel from [Solvespace] with Cython bundle.
    - [Pyslvs]: Kernel from [Sketch Solve] with Cython.

+ **Mechanical Synthesis**

    - **Number Synthesis**: Combine the attributes of mechanism.
    - **Structural Synthesis**: Cython algorithm used to find out structural possibilities of the mechanism.
    - **Dimensional Synthesis**: Kernel from the three Cython algorithms (rewrite).

+ **Others**

    - Cross three platforms.
    - CAD-like user interface.
    - Auto layout of generalized chain.
    - The code complies with PEP8.

# Documentation

The documentation of Pyslvs and kernel API are deployed on Readthedocs ([stable] / [latest]).

Or start it from source:

```bash
pip install mkdocs
pip install -r doc-requirements.txt
mkdocs serve
```

If you have any question, please post on GitHub issue or contact <pyslvs@gmail.com>.

[PyQt5]: https://www.riverbankcomputing.com/software/pyqt/download5
[Solvespace]: http://solvespace.com
[Python-Solvespace]: https://github.com/KmolYuan/solvespace
[Pyslvs]: https://github.com/KmolYuan/pyslvs
[Sketch Solve]: https://code.google.com/archive/p/sketchsolve/

[stable]: https://pyslvs-ui.readthedocs.io/en/stable/
[latest]: https://pyslvs-ui.readthedocs.io/en/latest/
