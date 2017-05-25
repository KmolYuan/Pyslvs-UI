# -*- coding: utf-8 -*-
import numpy
from ..kernel.kernel_getter import *

def generateProcess(path, upper, lowerVal, minAngle=0., maxAngle=360., type=0, maxGen=1500, report=.05):
    p = len(path)
    upperVal = upper+[maxAngle]*p
    lowerVal = lowerVal+[minAngle]*p
    Parm_num = p+9
    report = int(maxGen*report) if report<=1. else int(maxGen*report/100) if report<=maxGen else int(maxGen*.05)
    mechanismParams = {
        'Driving':'A',
        'Follower':'D',
        'Link':'L0,L1,L2,L3,L4',
        'Target':'E',
        'ExpressionName':'PLAP,PLLP,PLLP',
        'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
        'targetPath':path,
        'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
        'VARS':9,
        'formula':['PLAP','PLLP']}
    mechanismObj = build_planar(mechanismParams)
    if type==0:
        algorithmPrams = {
            'nParm':Parm_num,
            'nPop':250,
            'pCross':0.95,
            'pMute':0.05,
            'pWin':0.95,
            'bDelta':5.,
            'upper':upperVal,
            'lower':lowerVal,
            'maxGen':maxGen,
            'report':report}
        foo = Genetic(mechanismObj, **algorithmPrams)
    elif type==1:
        algorithmPrams = {
            'D':Parm_num,
            'n':40,
            'alpha':0.01,
            'betaMin':0.2,
            'gamma':1.,
            'beta0':1.,
            'ub':upperVal,
            'lb':lowerVal,
            'maxGen':maxGen,
            'report':report}
        foo = Firefly(mechanismObj, **algorithmPrams)
    elif type==2:
        algorithmPrams = {
            'strategy':1,
            'D':Parm_num,
            'NP':190,
            'F':0.6,
            'CR':0.9,
            'upper':upperVal,
            'lower':lowerVal,
            'maxGen':maxGen,
            'report':report}
        foo = DiffertialEvolution(mechanismObj, **algorithmPrams)
    time_and_fitness, fitnessParameter = foo.run()
    time_and_fitness = [float(k[1]) for k in [e.split(',') for e in time_and_fitness.split(';')[0:-1]]]
    fitnessParameter = [float(e) for e in fitnessParameter.split(',')]
    print('time_and_fitness: {}'.format(time_and_fitness))
    print('fitnessParameter: {}'.format(fitnessParameter))
    return time_and_fitness, fitnessParameter
