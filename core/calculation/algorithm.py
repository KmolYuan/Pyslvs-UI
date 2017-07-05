# -*- coding: utf-8 -*-
import numpy
from ..kernel.kernel_getter import *

def generateProcess(type_num, mechanismParams, GenerateData):
    mechanismObj = build_planar(mechanismParams)
    if type_num==0:
        algorithmPrams = {
            'nParm':GenerateData['nParm'],
            'nPop':250,
            'pCross':0.95,
            'pMute':0.05,
            'pWin':0.95,
            'bDelta':5.,
            'upper':GenerateData['upper'],
            'lower':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = Genetic(mechanismObj, **algorithmPrams)
    elif type_num==1:
        algorithmPrams = {
            'D':GenerateData['nParm'],
            'n':40,
            'alpha':0.01,
            'betaMin':0.2,
            'gamma':1.,
            'beta0':1.,
            'ub':GenerateData['upper'],
            'lb':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = Firefly(mechanismObj, **algorithmPrams)
    elif type_num==2:
        algorithmPrams = {
            'strategy':1,
            'D':GenerateData['nParm'],
            'NP':190,
            'F':0.6,
            'CR':0.9,
            'upper':GenerateData['upper'],
            'lower':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = DiffertialEvolution(mechanismObj, **algorithmPrams)
    time_and_fitness, fitnessParameter = foo.run()
    return([float(k[1]) for k in [e.split(',') for e in time_and_fitness.split(';')[0:-1]]],
        [float(e) for e in fitnessParameter.split(',')])
