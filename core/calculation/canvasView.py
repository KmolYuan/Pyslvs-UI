# -*- coding: utf-8 -*-
from .__init__ import *
from .canvasScene import DynamicScene

class DynamicCanvas(QGraphicsView):
    mouse_track = pyqtSignal(float, float)
    change_event = pyqtSignal()
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setParent(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setMouseTracking(True)
        self.scaleFactor=1
        self.Solve_error = False
        self.points = {
            'x':[], 'y':[], 'origin':{'x':self.width()/2, 'y':self.height()/2}, 'rate':2,
            'style':{
                'Background':Qt.white, 'penWidth':{'pen':2, 'path':1},
                'pt':Qt.green, 'link':Qt.darkGray, 'chain':Qt.cyan, 'text':Qt.darkGray,
                'dimension':False,
                },
            'Path':{'path':[], 'run_list':[], 'show':True},
            }
        self.Selector = {
            'Drag':{'x':0, 'y':0, 'isDrag':False},
            'Scanner':{'x':0, 'y':0, 'point':0, 'isClose':False},
            }
        self.AuxLine = {
            'show':False, 'pt':0,
            'horizontal':True, 'vertical':True, 'isMax':True, 'isMin':True,
            'color':6, 'limit_color':8,
            'Max':{'x':0, 'y':0}, 'Min':{'x':0, 'y':0},
            }
        self.Reset_Aux_limit()
        self.Color = {
            'Red':Qt.red,
            'Green':Qt.green,
            'Blue':Qt.blue,
            'Cyan':Qt.cyan,
            'Magenta':Qt.magenta,
            'Yellow':Qt.yellow,
            'Gray':Qt.gray,
            'Orange':QColor(225, 165, 0),
            'Pink':QColor(225, 192, 230),
            'Black':Qt.black,
            'White':Qt.white,
            'Dark Red':Qt.darkRed,
            'Dark Green':Qt.darkGreen,
            'Dark Blue':Qt.darkBlue,
            'Dark Cyan':Qt.darkCyan,
            'Dark Magenta':Qt.darkMagenta,
            'Dark Yellow':Qt.darkYellow,
            'Dark Gray':Qt.darkGray,
            'Dark Orange':QColor(225, 140, 0),
            'Dark Pink':QColor(225, 20, 147),
            }
        self.re_Color = [e for e in self.Color]
        self.scene = DynamicScene()
        self.setScene(self.scene)
    
    def update_figure(self, width, pathwidth,
            table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod, table_parameter,
            table_style, zoom_rate,
            Font_size, showDimension, Point_mark, Blackground):
        if not(self.Solve_error):
            if Blackground: self.points['style']['Background'] = Qt.black
            else: self.points['style']['Background'] = Qt.white
        else: self.points['style']['Background'] = QColor(102, 0, 0)
        self.Font_size = Font_size
        self.points['style']['dimension'] = showDimension
        self.Point_mark = Point_mark
        self.points['style']['penWidth']['pen'] = width
        self.points['style']['penWidth']['path'] = pathwidth
        self.points['x'] = []
        self.points['y'] = []
        self.zoom = float(zoom_rate.replace("%", ""))/100
        for i in range(len(table_point)):
            try:
                self.points['x'] += [table_point[i]['cx']*self.zoom*self.points['rate']]
                self.points['y'] += [table_point[i]['cy']*self.zoom*self.points['rate']*(-1)]
            except:
                self.points['x'] += [table_point[i]['x']*self.zoom*self.points['rate']]
                self.points['y'] += [table_point[i]['y']*self.zoom*self.points['rate']*(-1)]
        self.table_point = table_point
        self.table_line = table_line
        self.table_chain = table_chain
        self.table_shaft = table_shaft
        self.table_slider = table_slider
        self.table_rod = table_rod
        self.table_style = table_style
        self.update()
    
    def path_track(self, path, run_list):
        self.points['Path']['path'] = path
        self.points['Path']['run_list'] = run_list
        self.update()
    
    def Reset_Aux_limit(self):
        try:
            self.AuxLine['Max']['x'] = self.table_point[self.AuxLine['pt']]['cx']
            self.AuxLine['Max']['y'] = self.table_point[self.AuxLine['pt']]['cy']
            self.AuxLine['Min']['x'] = self.table_point[self.AuxLine['pt']]['cx']
            self.AuxLine['Min']['y'] = self.table_point[self.AuxLine['pt']]['cy']
        except:
            self.AuxLine['Max']['x'] = 0
            self.AuxLine['Max']['y'] = 0
            self.AuxLine['Min']['x'] = 0
            self.AuxLine['Min']['y'] = 0
    def removePath(self): self.points['Path']['path'] = []
    
    def wheelEvent(self, event):
        ''''''
    
    '''
    def mousePressEvent(self, event):
        if event.buttons()==Qt.MiddleButton:
            self.Selector['Drag']['x'] = event.x()-self.points['origin']['x']
            self.Selector['Drag']['y'] = event.y()-self.points['origin']['y']
            self.Selector['Drag']['isDrag'] = True
        elif QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.Selector['Drag']['x'] = 0
            self.Selector['Drag']['y'] = 0
            self.Selector['Drag']['isDrag'] = True
    def mouseReleaseEvent(self, event): self.Selector['Drag']['isDrag'] = False
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.points['origin']['x'] = event.x()
            self.points['origin']['y'] = event.y()
            self.update()
    def mouseMoveEvent(self, event):
        if self.Selector['Drag']['isDrag']:
            self.points['origin']['x'] = event.x()-self.Selector['Drag']['x']
            self.points['origin']['y'] = event.y()-self.Selector['Drag']['y']
            self.update()
        self.Selector['Scanner']['x'] = round((event.x()-self.points['origin']['x'])/self.zoom/self.points['rate'], 2)
        self.Selector['Scanner']['y'] = round((event.y()-self.points['origin']['y'])*(-1)/self.zoom/self.points['rate'], 2)
        self.mouse_track.emit(self.Selector['Scanner']['x'], self.Selector['Scanner']['y'])
    '''
