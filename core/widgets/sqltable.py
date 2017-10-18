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

tableName = "workbook"

class FileTable(QWidget):
    def __init__(self, parent):
        super(FileTable, self).__init__(parent)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(":memory:")
        db.open()
        #Qt example code!
        query = QSqlQuery(db)
        query.exec("create table {} (id int primary key, ".format(tableName)+
                   "firstname varchar(20), lastname varchar(20))")
        query.exec("insert into {} values(101, 'Danny', 'Young')".format(tableName))
        query.exec("insert into {} values(102, 'Christine', 'Holand')".format(tableName))
        query.exec("insert into {} values(103, 'Lars', 'Gordon')".format(tableName))
        query.exec("insert into {} values(104, 'Roberto', 'Robitaille')".format(tableName))
        query.exec("insert into {} values(105, 'Maria', 'Papadopoulos')".format(tableName))
        self.model = QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "First name")
        self.model.setHeaderData(2, Qt.Horizontal, "Last name")
        view = QTableView(self)
        view.setModel(self.model)
        view.resizeColumnsToContents()
        view.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mainLayout = QHBoxLayout(self)
        mainLayout.addWidget(view)
        self.setLayout(mainLayout)
    
    def save(self, fileName):
        #The database in memory.
        db = self.model.database()
        db.transaction()
        if self.model.submitAll():
            db.commit()
            print("Database Saved to memory.")
        else:
            db.rollback()
            print("Database Error!")
            print(self.model.lastError().databaseText())
        #The database in file.
        dbFile = QSqlDatabase.addDatabase("QSQLITE")
        dbFile.setDatabaseName(fileName)
        dbFile.open()
        destQuery = QSqlQuery(dbFile)
        #Copy data from memory.
        srcQuery = QSqlQuery(db)
        srcQuery.exec("SHOW CREATE TABLE {}".format(tableName))
        tableCreateStr = ""
        while srcQuery.next():
            tableCreateStr = srcQuery.value(1).toString()
        #Clear the file table.
        destQuery.exec("DROP TABLE IF EXISTS {}".format(tableName))
        destQuery.exec(tableCreateStr)
        srcQuery.exec("SELECT * FROM {}".format(tableName))
        while srcQuery.next():
            record = srcQuery.record()
            names = []
            placeholders = []
            values = []
            for i in range(record.count()):
                names.append(record.fieldName(i))
                placeholders.append(':' + record.fieldName(i))
                value = srcQuery.value(i)
                if value.type()==QVariant.String:
                    values.append("\"{}\"".format(value.toString()))
                else:
                    values.append(value)
            destQuery.prepare(
                "INSERT INTO {} ({}) VALUES ({})".format(tableName, ", ".join(names), ", ".join(placeholders))
            )
            for value in values:
                destQuery.addBindValue(value)
            destQuery.exec()
        dbFile.close()
        print("Database Saved.")
