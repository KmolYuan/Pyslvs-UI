# -*- coding: utf-8 -*-
import numpy
from ..kernel.kernel_getter import *

def generateProcess(type_num, mechanismParams, GenerateData, algorithmPrams):
    mechanismObj = build_planar(mechanismParams)
    #Genetic Algorithm
    if type_num==0:
        APs = {
            'nParm':GenerateData['nParm'],
            'nPop':algorithmPrams['nPop'], #250
            'pCross':algorithmPrams['pCross'], #0.95
            'pMute':algorithmPrams['pMute'], #0.05
            'pWin':algorithmPrams['pWin'], #0.95
            'bDelta':algorithmPrams['bDelta'], #5.
            'upper':GenerateData['upper'],
            'lower':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = Genetic(mechanismObj, **APs)
    #Firefly Algorithm
    elif type_num==1:
        APs = {
            'D':GenerateData['nParm'],
            'n':algorithmPrams['n'], #40
            'alpha':algorithmPrams['alpha'], #0.01
            'betaMin':algorithmPrams['betaMin'], #0.2
            'gamma':algorithmPrams['gamma'], #1.
            'beta0':algorithmPrams['beta0'], #1.
            'ub':GenerateData['upper'],
            'lb':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = Firefly(mechanismObj, **APs)
    #Differential Evolution
    elif type_num==2:
        APs = {
            'D':GenerateData['nParm'],
            'strategy':algorithmPrams['strategy'], #1
            'NP':algorithmPrams['NP'], #190
            'F':algorithmPrams['F'], #0.6
            'CR':algorithmPrams['CR'], #0.9
            'upper':GenerateData['upper'],
            'lower':GenerateData['lower'],
            'maxGen':GenerateData['maxGen'],
            'report':GenerateData['report']}
        foo = DiffertialEvolution(mechanismObj, **APs)
    time_and_fitness, fitnessParameter = foo.run()
    return([float(k[1]) for k in [e.split(',') for e in time_and_fitness.split(';')[0:-1]]],
        [float(e) for e in fitnessParameter.split(',')])
