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

from ..libs.pyslvs_algorithm import tinycadlib
from ..libs.pyslvs_algorithm.planarlinkage import build_planar
import os, zmq

def startRep(PORT):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(PORT) #tcp://localhost:8000
    print("The server starts.\nYou can using Ctrl + C to terminate.")
    print("Address: {}".format(PORT))
    print("Worker {} is awaiting orders...".format(os.getpid(), PORT))
    while True:
        try:
            data = socket.recv().decode("utf-8").split(';')
            mechanismParams = {
                'Driving':data[0],
                'Follower':data[1],
                'Link':data[2],
                'Target':data[3],
                'ExpressionName':data[4],
                'Expression':data[5],
                'targetPath':tuple(tuple(float(k) for k in e.split(':')) for e in data[6].split(',')),
                'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
                'formula':['PLAP','PLLP']}
            mechanismParams['VARS'] = len(set(mechanismParams['Expression'].split(',')))-2
            mechanismObj = build_planar(mechanismParams)
            print([float(e) for e in data[7].split(',')])
            fitness = mechanismObj([float(e) for e in data[7].split(',')])
            socket.send_string(str(fitness))
            print("Fitness: {}".format(fitness), end='\r')
        except KeyboardInterrupt:
            print("W: interrupt received, stopping...")
            break
    socket.close()
    context.term()
