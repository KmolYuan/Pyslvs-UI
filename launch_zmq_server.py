# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]

if __name__=='__main__':
    from core.server.zmq_rep import startRep
    startRep("tcp://localhost:8000")
    exit()
