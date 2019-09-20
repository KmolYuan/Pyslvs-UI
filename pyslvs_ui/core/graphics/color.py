# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from qtpy.QtCore import QSize
from qtpy.QtGui import QColor, QIcon, QPixmap
from pyslvs import color_names, color_rgb


def color_qt(name: str) -> QColor:
    """Get color and translate to QColor."""
    return QColor(*color_rgb(name))


def color_num(color_index: int) -> QColor:
    """Get color by index."""
    return color_qt(color_names[color_index % len(color_names)])


def color_icon(name: str, size: int = 20) -> QIcon:
    """Get color block as QIcon by name."""
    color_block = QPixmap(QSize(size, size))
    color_block.fill(color_qt(name))
    return QIcon(color_block)


# Target path color: (road, dot, brush)
_path_color = (
    # Blue - Green
    (QColor(69, 247, 232), QColor(3, 163, 120), QColor(74, 178, 176, 30)),
    # Yellow - Green
    (QColor(187, 221, 75), QColor(103, 124, 12), QColor(242, 242, 4, 30)),
    # Red - Yellow
    (QColor(252, 110, 27), QColor(237, 129, 66), QColor(242, 158, 109, 30)),
    # Purple - Blue
    (QColor(115, 0, 145), QColor(220, 104, 249), QColor(198, 137, 214, 30))
)


def target_path_style(color_index: int) -> QColor:
    """Get path colors."""
    return _path_color[color_index % len(_path_color)]
