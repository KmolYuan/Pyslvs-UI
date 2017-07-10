# -*- coding: utf-8 -*-
import time, timeit
import zmq
from .rga import Genetic

def startReq(PORT):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.bind(PORT) #tcp://localhost:8000
    time.sleep(1)
    path = tuple((i, i) for i in range(11))
    p = len(path)
    VARS = 9
    Parm_num = p+VARS
    mechanismParams = {
        'Driving':'A',
        'Follower':'D',
        'Link':'L0,L1,L2,L3,L4',
        'Target':'E',
        'ExpressionName':'PLAP,PLLP,PLLP',
        'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
        'VARS':VARS,
        'targetPath':path,
        'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
        'formula':['PLAP','PLLP']}
    APs = {
        'nParm':Parm_num,
        'nPop':250, #250
        'pCross':0.95, #0.95
        'pMute':0.05, #0.05
        'pWin':0.95, #0.95
        'bDelta':5., #5.
        'upper':[50,50,50,50,50,50,50,50,50] + [360.0] * p,
        'lower':[-50,-50,-50,-50, 5, 5, 5, 5, 5] + [0.0] * p,
        'maxGen':1500,
        'report':500}
    foo = Genetic(mechanismParams, socket=socket, **APs)
    t0 = timeit.default_timer()
    foo.run()
    t1 = timeit.default_timer()
    print('total cost time: {}'.format(t1-t0))
