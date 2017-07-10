# -*- coding: utf-8 -*-
from ..kernel.kernel_getter import build_planar

def startRep(PORT):
    import os, zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(PORT) #tcp://localhost:8000
    print("Address: {}".format(PORT))
    print("Worker {} is awaiting orders...".format(os.getpid(), PORT))
    while True:
        mechanismParams, Chrom_v = socket.recv_pyobj()
        mechanismObj = build_planar(mechanismParams)
        fitness = mechanismObj(Chrom_v)
        socket.send_pyobj(fitness)
