# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
def colorlist():
    return {
        "Red":QColor(172, 68, 68),
        "Green":QColor(110, 190, 30),
        "Blue":QColor(68, 120, 172),
        "Cyan":Qt.cyan,
        "Magenta":QColor(255, 130, 130),
        "Yellow":Qt.yellow,
        "Gray":Qt.gray,
        "Orange":QColor(225, 165, 0),
        "Pink":QColor(225, 192, 230),
        "Black":Qt.black,
        "White":Qt.white,
        "Dark-Red":Qt.darkRed,
        "Dark-Green":Qt.darkGreen,
        "Dark-Blue":Qt.darkBlue,
        "Dark-Cyan":Qt.darkCyan,
        "Dark-Magenta":Qt.darkMagenta,
        "Dark-Yellow":Qt.darkYellow,
        "Dark-Gray":Qt.darkGray,
        "Dark-Orange":QColor(225, 140, 0),
        "Dark-Pink":QColor(225, 20, 147),
        }
def colorName(): return sorted(list(colorlist().keys()))
