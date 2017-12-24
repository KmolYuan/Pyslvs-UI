# -*- coding: utf-8 -*-
from libc.math cimport fmod, pow
import numpy as np
cimport numpy as np
#from libc.time cimport time
from time import time as pytime
from cpython.exc cimport PyErr_CheckSignals
from cpython cimport bool

#https://stackoverflow.com/questions/25974975/cython-c-array-initialization
from libc.stdlib cimport rand, RAND_MAX, srand
srand(int(pytime()))

cdef double randV():
    return rand()/(RAND_MAX*1.01)

cdef class Chromosome(object):
    cdef public int n
    cdef public double f
    cdef public np.ndarray v
    
    def __cinit__(self, int n):
        self.n = n if n > 0 else 2
        self.f = 0.0
        self.v = np.zeros(n)
    
    def cp(self, Chromosome obj):
        """
        copy all atribute from another chromsome object
        """
        self.n = obj.n
        self.f = obj.f
        self.v[:] = obj.v
    
    def is_self(self, obj):
        """
        check the object is self?
        """
        return obj is self
    
    def assign(self, obj):
        if not self.is_self(obj):
            self.cp(obj)

cdef class Genetic(object):
    cdef int nParm, nPop, maxGen, gen, rpt
    cdef double pCross, pMute, pWin, bDelta, iseed, mask, seed, timeS, timeE
    cdef object func, progress_fun, interrupt_fun
    cdef np.ndarray chrom, newChrom, babyChrom
    cdef Chromosome chromElite, chromBest
    cdef np.ndarray maxLimit, minLimit
    cdef object fitnessTime, fitnessParameter
    
    def __cinit__(self, object objFunc, int nParm, int nPop,
            double pCross, double pMute, double pWin, double bDelta, object upper, object lower,
            int maxGen, int report, object progress_fun=None, object interrupt_fun=None):
        """
        init(function func)
        """
        # check nParm and list upper's len is equal
        if nParm != len(upper) or nParm != len(lower):
            raise Exception("nParm and upper's length and lower's length must be equal")
        self.func = objFunc
        self.nParm = nParm
        self.nPop = nPop
        self.pCross = pCross
        self.pMute = pMute
        self.pWin = pWin
        self.bDelta = bDelta
        self.maxGen = maxGen
        self.rpt = report
        self.progress_fun = progress_fun
        self.interrupt_fun = interrupt_fun
        
        self.chrom = np.ndarray((nPop,),dtype=np.object)
        for i in range(nPop):
            self.chrom[i] = Chromosome(self.nParm)
        self.newChrom = np.ndarray((nPop,),dtype=np.object)
        for i in range(nPop):
            self.newChrom[i] = Chromosome(self.nParm)
        self.babyChrom = np.ndarray((3,),dtype=np.object)
        for i in range(3):
            self.babyChrom[i] = Chromosome(self.nParm)
        
        self.chromElite = Chromosome(nParm)
        self.chromBest = Chromosome(nParm)
        # low bound
        self.minLimit = np.array(lower[:])
        # up bound
        self.maxLimit = np.array(upper[:])
        # maxgen and gen
        self.gen = 0
        
        # setup benchmark
        self.timeS = pytime()
        self.timeE = 0
        self.fitnessTime = ''
        self.fitnessParameter = ''
    
    cdef int random(self, int k)except *:
        return int(randV()*k)
    
    cdef double randVal(self, double low, double high)except *:
        return randV()*(high-low)+low
    
    cdef double check(self, int i, double v)except *:
        """
        If a variable is out of bound,
        replace it with a random value
        """
        if (v > self.maxLimit[i]) or (v < self.minLimit[i]):
            return self.randVal(self.minLimit[i], self.maxLimit[i])
        return v
    
    cdef void crossOver(self)except *:
        cdef int i, s, j
        for i in range(0, self.nPop-1, 2):
            # crossover
            if(randV() < self.pCross):
                for s in range(self.nParm):
                    # first baby, half father half mother
                    self.babyChrom[0].v[s] = 0.5 * self.chrom[i].v[s] + 0.5*self.chrom[i+1].v[s];
                    # second baby, three quaters of fater and quater of mother
                    self.babyChrom[1].v[s] = self.check(s, 1.5 * self.chrom[i].v[s] - 0.5*self.chrom[i+1].v[s])
                    # third baby, quater of fater and three quaters of mother
                    self.babyChrom[2].v[s] = self.check(s,-0.5 * self.chrom[i].v[s] + 1.5*self.chrom[i+1].v[s]);
                # evaluate new baby
                for j in range(3):
                    self.babyChrom[j].f = self.func(self.babyChrom[j].v)
                # maybe use bubble sort? smaller -> larger
                if self.babyChrom[1].f < self.babyChrom[0].f:
                    self.babyChrom[0], self.babyChrom[1] = self.babyChrom[1], self.babyChrom[0]
                if self.babyChrom[2].f < self.babyChrom[0].f:
                    self.babyChrom[2], self.babyChrom[0] = self.babyChrom[0], self.babyChrom[2]
                if self.babyChrom[2].f < self.babyChrom[1].f:
                    self.babyChrom[2], self.babyChrom[1] = self.babyChrom[1], self.babyChrom[2]
                # replace first two baby to parent, another one will be
                self.chrom[i].assign(self.babyChrom[0])
                self.chrom[i+1].assign(self.babyChrom[1])
    
    cdef double delta(self, double y)except *:
        cdef double r
        r = self.gen / self.maxGen
        return y*randV()*pow(1.0-r, self.bDelta)
    
    cdef void fitness(self)except *:
        cdef int j
        for j in range(self.nPop):
            self.chrom[j].f = self.func(self.chrom[j].v)
        self.chromBest.assign(self.chrom[0])
        for j in range(1, self.nPop):
            if(self.chrom[j].f < self.chromBest.f):
                self.chromBest.assign(self.chrom[j])
        if(self.chromBest.f < self.chromElite.f):
            self.chromElite.assign(self.chromBest)
    
    cdef void initialPop(self)except *:
        cdef int i, j
        for j in range(self.nPop):
            for i in range(self.nParm):
                self.chrom[j].v[i] = self.randVal(self.minLimit[i], self.maxLimit[i])
    
    cdef void mutate(self)except *:
        cdef int i, s
        for i in range(self.nPop):
            if randV() < self.pMute:
                s = self.random(self.nParm)
                if (self.random(2) == 0):
                    self.chrom[i].v[s] += self.delta(self.maxLimit[s]-self.chrom[i].v[s])
                else:
                    self.chrom[i].v[s] -= self.delta(self.chrom[i].v[s]-self.minLimit[s])
    
    cdef void report(self)except *:
        self.timeE = pytime()
        self.fitnessTime += '%d,%.4f,%.2f;'%(self.gen, self.chromElite.f, self.timeE - self.timeS)
    
    cdef void select(self)except *:
        """
        roulette wheel selection
        """
        cdef int i, j, k
        for i in range(self.nPop):
            j = self.random(self.nPop)
            k = self.random(self.nPop)
            self.newChrom[i].assign(self.chrom[j])
            if(self.chrom[k].f < self.chrom[j].f) and (randV() < self.pWin):
                self.newChrom[i].assign(self.chrom[k])
        # in this stage, newChrom is select finish
        # now replace origin chrom
        for i in range(self.nPop):
            self.chrom[i].assign(self.newChrom[i])
        # select random one chrom to be best chrom, make best chrom still exist
        j = self.random(self.nPop);
        self.chrom[j].assign(self.chromElite)
    
    cdef void getParamValue(self):
        self.fitnessParameter = ','.join(['%.4f'%(v) for v in self.chromElite.v])
    
    cdef void generation_process(self):
        self.select()
        self.crossOver()
        self.mutate()
        self.fitness()
        if self.rpt != 0:
            if self.gen % self.rpt == 0:
                self.report()
        else:
            if self.gen % 10 == 0:
                self.report()
        #progress
        if self.progress_fun is not None:
            self.progress_fun(self.gen, '%.4f'%self.chromElite.f)
    
    cpdef run(self):
        """
        // **** Init and run GA for maxGen times
        // **** mxg : maximum generation
        // **** rp  : report cycle, 0 for final report or
        // ****       report each mxg modulo rp
        """
        self.initialPop()
        self.chrom[0].f = self.func(self.chrom[0].v)
        self.chromElite.assign(self.chrom[0])
        self.gen = 0
        self.fitness()
        self.report()
        if self.maxGen>0:
            for self.gen in range(1, self.maxGen+1):
                self.generation_process()
                #interrupt
                if self.interrupt_fun is not None:
                    if self.interrupt_fun():
                        break
                PyErr_CheckSignals()
        else:
            while True:
                self.generation_process()
                self.gen += 1
                #interrupt
                if self.interrupt_fun is not None:
                    if self.interrupt_fun():
                        break
                PyErr_CheckSignals()
        self.report()
        self.getParamValue()
        return self.fitnessTime, self.fitnessParameter
