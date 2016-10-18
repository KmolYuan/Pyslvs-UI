import csv
from .dxf_type import dxf_code

class Transfer():
    def __init__(self):
        self.Entiteis_Point = []
        self.Entiteis_Point_Style = []
        self.Entiteis_Link = []
        self.Entiteis_Stay_Chain = []
        self.Drive_Shaft = []
        self.Slider = []
        self.Rod = []
        self.Parameter_list = []
    
    def input_file(self, fileName):
        self.fileName = fileName
        print("Get:"+fileName)
        data = []
        with open(fileName, newline="") as stream:
            reader = csv.reader(stream, delimiter=' ', quotechar='|')
            for row in reader: data += ', '.join(row).split('\t,')
        bookmark = 0
        for i in range(4, len(data), 4):
            bookmark = i
            if '_' in data[i]: break
            fixed = data[i+3]=="Fixed"
            self.Entiteis_Point += [data[i+1], data[i+2], fixed]
        self.Entiteis_Point_Style.removeRow(0)
        for i in range(bookmark+1, len(data), 4):
            bookmark = i
            if '_' in data[i]: break
            self.Entiteis_Point_Style += [data[i+1], data[i+2], data[i+3]]
        for i in range(bookmark+1, len(data), 4):
            bookmark = i
            if '_' in data[i]: break
            self.Entiteis_Link += [data[i+1], data[i+2], data[i+3]]
        for i in range(bookmark+1, len(data), 7):
            bookmark = i
            if '_' in data[i]: break
            self.Entiteis_Stay_Chain += [data[i+1], data[i+2], data[i+3], data[i+4], data[i+5], data[i+6]]
        for i in range(bookmark+1, len(data), 6):
            bookmark = i
            if '_' in data[i]: break
            self.Drive_Shaft += [data[i+1], data[i+2], data[i+3], data[i+4], data[i+5]]
        for i in range(bookmark+1, len(data), 3):
            bookmark = i
            if '_' in data[i]: break
            self.Slider += [data[i+1], data[i+2]]
        for i in range(bookmark+1, len(data), 5):
            bookmark = i
            if '_' in data[i]: break
            self.Rod += [data[i+1], data[i+2], data[i+3], data[i+4]]
        for i in range(bookmark+1, len(data), 3):
            bookmark = i
            if '_' in data[i]: break
            self.Parameter_list += [data[i+1], data[i+2]]
    
    def show_dxf(self):
        print("Saving to DXF...")
        dxf_code(self.fileName, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Drive_Shaft, self.Slider, self.Rod)
