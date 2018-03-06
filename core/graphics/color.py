# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QColor,
    Qt,
    QIcon,
    QPixmap,
    QSize,
)
from typing import Tuple

"""Color dictionary."""
color_list = {
    'Red': QColor(172, 68, 68),
    'Green': QColor(110, 190, 30),
    'Blue': QColor(68, 120, 172),
    'Cyan': Qt.cyan,
    'Magenta': Qt.magenta,
    'Brick-Red': QColor(255, 130, 130),
    'Yellow': Qt.yellow,
    'Gray': Qt.gray,
    'Orange': QColor(225, 165, 0),
    'Pink': QColor(225, 192, 230),
    'Black': Qt.black,
    'White': Qt.white,
    'Dark-Red': Qt.darkRed,
    'Dark-Green': Qt.darkGreen,
    'Dark-Blue': Qt.darkBlue,
    'Dark-Cyan': Qt.darkCyan,
    'Dark-Magenta': Qt.darkMagenta,
    'Dark-Yellow': Qt.darkYellow,
    'Dark-Gray': Qt.darkGray,
    'Dark-Orange': QColor(225, 140, 0),
    'Dark-Pink': QColor(225, 20, 147),
}

def colorName() -> Tuple[str]:
    """Get color names."""
    return tuple(sorted(color_list.keys()))

def colorQt(colorName: str) -> QColor:
    """Get color by name."""
    return color_list.get(colorName, color_list['Blue'])

def colorNum(colorIndex: int) -> QColor:
    """Get color by index."""
    return color_list[colorName()[colorIndex % len(color_list)]]

def colorIcons(colorName: str, size: int =20) -> QIcon:
    """Get color block as QIcon by name."""
    colorBlock = QPixmap(QSize(size, size))
    colorBlock.fill(colorQt(colorName))
    return QIcon(colorBlock)

"""Target path color.

(Pen, Dot, Brush)
"""
path_color = (
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
    return path_color[colorIndex % len(path_color)]
