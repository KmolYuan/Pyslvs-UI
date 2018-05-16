# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QColor,
    QIcon,
    QPixmap,
    QSize,
)
from core.libs import colorNames, colorRGB


def colorQt(name: str) -> QColor:
    """Get color and translate to QColor."""
    return QColor(*colorRGB(name))


def colorNum(colorIndex: int) -> QColor:
    """Get color by index."""
    return colorQt(colorNames[colorIndex % len(colorNames)])


def colorIcon(name: str, size: int = 20) -> QIcon:
    """Get color block as QIcon by name."""
    colorBlock = QPixmap(QSize(size, size))
    colorBlock.fill(colorQt(name))
    return QIcon(colorBlock)


#Target path color: (Pen, Dot, Brush)
_path_color = (
    #Blue - Green
    (QColor(69, 247, 232), QColor(3, 163, 120), QColor(74, 178, 176, 30)),
    #Yellow - Green
    (QColor(187, 221, 75), QColor(103, 124, 12), QColor(242, 242, 4, 30)),
    #Red - Yellow
    (QColor(252, 110, 27), QColor(237, 129, 66), QColor(242, 158, 109, 30)),
    #Purple - Blue
    (QColor(115, 0, 145), QColor(220, 104, 249), QColor(198, 137, 214, 30))
)


def colorPath(colorIndex: int) -> QColor:
    """Get path colors."""
    return _path_color[colorIndex % len(_path_color)]
