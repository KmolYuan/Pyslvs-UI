# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from core.QtModules import *
from typing import Tuple

#Color dictionary.
color_list = {
    'Red':QColor(172, 68, 68),
    'Green':QColor(110, 190, 30),
    'Blue':QColor(68, 120, 172),
    'Cyan':Qt.cyan,
    'Magenta':Qt.magenta,
    'Brick-Red':QColor(255, 130, 130),
    'Yellow':Qt.yellow,
    'Gray':Qt.gray,
    'Orange':QColor(225, 165, 0),
    'Pink':QColor(225, 192, 230),
    'Black':Qt.black,
    'White':Qt.white,
    'Dark-Red':Qt.darkRed,
    'Dark-Green':Qt.darkGreen,
    'Dark-Blue':Qt.darkBlue,
    'Dark-Cyan':Qt.darkCyan,
    'Dark-Magenta':Qt.darkMagenta,
    'Dark-Yellow':Qt.darkYellow,
    'Dark-Gray':Qt.darkGray,
    'Dark-Orange':QColor(225, 140, 0),
    'Dark-Pink':QColor(225, 20, 147),
}

#Get color names.
def colorName() -> Tuple[str]:
    return tuple(sorted(color_list.keys()))

#Get color by name.
def colorQt(colorName: str) -> QColor:
    return color_list.get(colorName, color_list['Blue'])

#Get color by index.
def colorNum(colorIndex: int) -> QColor:
    return color_list[colorName()[colorIndex % len(color_list)]]

#Get color block as QIcon by name.
def colorIcons(colorName: str, size: int =20) -> QIcon:
    colorBlock = QPixmap(QSize(size, size))
    colorBlock.fill(colorQt(colorName))
    return QIcon(colorBlock)

#Target path color.
#(Pen, Dot, Brush)
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

#Get path colors.
def colorPath(colorIndex: int) -> QColor:
    return path_color[colorIndex % len(path_color)]
