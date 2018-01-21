# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
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
colorlist = {
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
    return tuple(sorted(colorlist.keys()))

#Get color by name.
def colorQt(colorName: str) -> QColor:
    return colorlist.get(colorName, colorlist['Blue'])

#Get color by index.
def colorNum(colorIndex: int) -> QColor:
    return colorlist[colorName()[colorIndex % len(colorlist.keys())]]

#Get color block as QIcon by name.
def colorIcons(colorName: str, size: int =20) -> QIcon:
    colorBlock = QPixmap(QSize(size, size))
    colorBlock.fill(colorQt(colorName))
    return QIcon(colorBlock)
