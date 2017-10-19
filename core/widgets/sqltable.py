# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
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

from ..QtModules import *
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    DateTimeField
)

class WorkbookBase(Model):
    #Field here.
    author = CharField(unique=True)
    commitText = TextField()
    date = DateTimeField()

class FileTable(QTableWidget):
    def __init__(self, parent):
        super(FileTable, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def save(self, fileName):
        db = SqliteDatabase(fileName)
        class Workbook(WorkbookBase):
            class Meta:
                database = db
        db.connect()
        db.create_tables([Workbook], safe=True)
        with db.atomic():
            try:
                #TODO: Save database.
                db.save()
            except:
                db.rollback()
        db.close()
    
    def read(self, fileName):
        db = SqliteDatabase(fileName)
        class Workbook(WorkbookBase):
            class Meta:
                database = db
        db.connect()
        db.create_tables([Workbook], safe=True)
        #TODO: Read and return database.
        db.close()
        return
