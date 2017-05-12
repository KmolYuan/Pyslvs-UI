# -*- coding: utf-8 -*-
from ..QtModules import *
def colorlist():
    return {
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
def colorName(): return sorted(list(colorlist().keys()))

def colorIcons():
    colors = colorlist()
    names = colorName()
    blocks = dict()
    for name in names:
        colorBlock = QPixmap(QSize(*([20]*2)))
        colorBlock.fill(colors[name])
        blocks.update({name:QIcon(colorBlock)})
    return blocks
