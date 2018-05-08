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


#Color dictionary.
_color_list = {
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

colorNames = tuple(sorted(_color_list.keys()))


def colorQt(name: str) -> QColor:
    """Get color by name."""
    if name in _color_list:
        return _color_list[name]
    else:
        #Input RGB as a "(255, 255, 255)" string.
        r, g, b = tuple(int(i) for i in (
            name.replace('(', '')
            .replace(')', '')
            .replace(" ", '')
            .split(',')
        ))
        return QColor(r, g, b)


def colorNum(colorIndex: int) -> QColor:
    """Get color by index."""
    return _color_list[colorNames[colorIndex % len(_color_list)]]


def colorIcon(name: str, size: int =20) -> QIcon:
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
