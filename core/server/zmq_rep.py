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

from ..kernel.kernel_getter import build_planar

mechanismParams_4Bar = { #No 'targetPath'
    'Driving':'A',
    'Follower':'D',
    'Link':'L0,L1,L2,L3,L4',
    'Target':'E',
    'ExpressionName':'PLAP,PLLP,PLLP',
    'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
    'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
    'formula':['PLAP','PLLP']}
mechanismParams_4Bar['VARS'] = len(set(mechanismParams_4Bar['Expression'].split(',')))-2
mechanismParams_8Bar = { #No 'targetPath'
    'Driving':'A',
    'Follower':'B',
    'Link':'L0,L1,L2,L3,L4,L5,L6,L7,L8,L9,L10',
    'Target':'H',
    'ExpressionName':'PLAP,PLLP,PLLP,PLLP,PLLP,PLLP',
    'Expression':'A,L0,a0,B,C,B,L2,L1,C,D,B,L4,L3,D,E,C,L5,L6,B,F,F,L8,L7,E,G,F,L9,L10,G,H',
    'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
    'formula':['PLAP','PLLP']}
mechanismParams_8Bar['VARS'] = len(set(mechanismParams_8Bar['Expression'].split(',')))-2

def startRep(PORT):
    import os, zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(PORT) #tcp://localhost:8000
    print("Address: {}".format(PORT))
    print("Worker {} is awaiting orders...".format(os.getpid(), PORT))
    while True:
        data = socket.recv().decode("utf-8").split(';')
        bar_type = data[0]
        Chrom_v = [float(e) for e in data[1].split(',')]
        targetPath = tuple(tuple(float(k) for k in e.split(':')) for e in data[2].split(','))
        mechanismParams = mechanismParams_4Bar if int(bar_type)==4 else mechanismParams_8Bar
        mechanismParams['targetPath'] = targetPath
        mechanismObj = build_planar(mechanismParams)
        fitness = mechanismObj(Chrom_v)
        socket.send_string(str(fitness))
