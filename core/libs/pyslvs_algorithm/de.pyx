# -*- coding: utf-8 -*-

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from cpython cimport bool
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, RAND_MAX, srand
#from libc.time cimport time
from time import time

#Make sure it is 'random'.
srand(int(time()))

cdef double randV():
    return rand()/(RAND_MAX*1.01)

cdef enum limit:
    maxGen,
    minFit,
    maxTime

cdef class Chromosome(object):
    
    cdef public int n
    cdef public double f
    cdef public np.ndarray v
    
    def __cinit__(self, int n):
        # dimension
        self.n = n
        # the gene
        self.v = np.zeros(n)
        # the fitness value
        self.f = 0
    
    cpdef void assign(self, Chromosome obj):
        self.n = obj.n
        self.v[:] = obj.v
        self.f = obj.f

cdef class DiffertialEvolution(object):
    
    cdef limit option
    cdef int strategy, D, NP, maxGen, maxTime, rpt, gen, r1, r2, r3, r4, r5
    cdef double F, CR, timeS, timeE, minFit
    cdef np.ndarray lb, ub, pop
    cdef object func, progress_fun, interrupt_fun
    cdef Chromosome lastgenbest, currentbest
    cdef list fitnessTime
    
    def __cinit__(self, object func, dict settings, object progress_fun=None, object interrupt_fun=None):
        """
        settings = {
            'strategy',
            'NP',
            'F',
            'CR',
            'maxGen', 'minFit' or 'maxTime',
            'report'
        }
        """
        # object function, or enviorment
        self.func = func
        # dimesion of quesiton
        self.D = self.func.get_nParm()
        # strategy 1~10, choice what strategy to generate new member in temporary
        self.strategy = settings['strategy']
        # population size
        # To start off NP = 10*D is a reasonable choice. Increase NP if misconvergence
        self.NP = settings['NP']
        # weight factor
        # F is usually between 0.5 and 1 (in rare cases > 1)
        self.F = settings['F']
        # crossover possible
        # CR in [0,1]
        self.CR = settings['CR']
        # low bound
        self.lb = np.array(self.func.get_lower())
        # up bound
        self.ub = np.array(self.func.get_upper())
        #Algorithm will stop when the limitation has happend.
        self.maxGen = 0
        self.minFit = 0
        self.maxTime = 0
        if 'maxGen' in settings:
            self.option = maxGen
            self.maxGen = settings['maxGen']
        elif 'minFit' in settings:
            self.option = minFit
            self.minFit = settings['minFit']
        elif 'maxTime' in settings:
            self.option = maxTime
            self.maxTime = settings['maxTime']
        else:
            raise Exception("Please give 'maxGen', 'minFit' or 'maxTime' limit.")
        #Report function
        self.rpt = settings['report']
        self.progress_fun = progress_fun
        self.interrupt_fun = interrupt_fun
        # check parameter is set properly
        self.checkParameter()
        # generation pool, depend on population size
        self.pop = np.ndarray((self.NP,), dtype=np.object)
        for i in range(self.NP):
            self.pop[i] = Chromosome(self.D)
        # last generation best member
        self.lastgenbest = Chromosome(self.D)
        # current best member
        self.currentbest = Chromosome(self.D)
        # the generation count
        self.gen = 0
        # the vector
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        self.r5 = 0
        
        # setup benchmark
        self.timeS = time()
        self.timeE = 0
        self.fitnessTime = []
    
    cdef void checkParameter(self):
        """
        check parameter is set properly
        """
        if (type(self.D) is not int) and self.D <= 0:
            raise Exception('D shoud be integer and larger than 0')
        if (type(self.NP) is not int) and self.NP <= 0:
            raise Exception('NP shoud be integer and larger than 0')
        if self.CR < 0 or self.CR > 1:
            raise Exception('CR should be [0,1]')
        if self.strategy < 1 or self.strategy > 10:
            raise Exception('strategy should be [1,10]')
        for lower, upper in zip(self.lb, self.ub):
            if lower > upper:
                raise Exception('upper bound should be larger than lower bound')
    
    cdef void init(self):
        """
        init population
        """
        cdef int i, j
        for i in range(self.NP):
            for j in range(self.D):
                self.pop[i].v[j] = self.lb[j] + randV()*(self.ub[j] - self.lb[j])
            self.pop[i].f = self.evalute(self.pop[i])
    
    cdef double evalute(self, Chromosome member):
        """
        evalute the member in enviorment
        """
        return self.func(member.v)
    
    cdef Chromosome findBest(self):
        """
        find member that have minimum fitness value from pool
        """
        cdef int i
        cdef int index = 0
        cdef Chromosome chrom
        cdef double f = self.pop[0].f
        for i in range(len(self.pop)):
            chrom = self.pop[i]
            if chrom.f < f:
                index = i
                f = chrom.f
        return self.pop[index]
    
    cdef void generateRandomVector(self, int i):
        """
        generate new vector
        """
        while True:
            self.r1 = int(randV() * self.NP)
            if self.r1 != i:
                break
        while True:
            self.r2 = int(randV() * self.NP)
            if (self.r2 != i) and (self.r2 != self.r1):
                break
        while True:
            self.r3 = int(randV() * self.NP)
            if (self.r3 != i) and (self.r3 != self.r1) and (self.r3 != self.r2):
                break
        while True:
            self.r4 = int(randV() * self.NP)
            if (self.r4 != i) and (self.r4 != self.r1) and (self.r4 != self.r2) and (self.r4 != self.r3):
                break
        while True:
            self.r5 = int(randV() * self.NP)
            if (self.r5 != i) and (self.r5 != self.r1) and (self.r5 != self.r2) and (self.r5 != self.r3) and (self.r5 != self.r4):
                break
    
    cdef Chromosome recombination(self, int i):
        """
        use new vector, recombination the new one member to tmp
        """
        cdef Chromosome tmp = Chromosome(self.D)
        tmp.assign(self.pop[i])
        cdef int n = int(randV() * self.D)
        cdef int L = 0
        if self.strategy==1:
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not (randV() < self.CR and L < self.D):
                    break
        elif self.strategy==2:
            while True:
                tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not (randV() < self.CR and L < self.D):
                    break
        elif self.strategy==3:
            while True:
                tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
                L += 1
                if not (randV() < self.CR and L < self.D):
                    break
        elif self.strategy==4:
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not (randV() < self.CR and L < self.D):
                    break
        elif self.strategy==5:
            while True:
                tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not (randV() < self.CR and L < self.D):
                    break
        elif self.strategy==6:
            for L in range(self.D):
                if (randV() < self.CR or L == self.D-1):
                    tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif self.strategy==7:
            for L in range(self.D):
                if ((randV() < self.CR) or L == self.D-1):
                    tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif self.strategy==8:
            for L in range(self.D):
                if (randV() < self.CR or L == self.D-1):
                    tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
        elif self.strategy==9:
            for L in range(self.D):
                if (randV() < self.CR or L == self.D-1):
                    tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        else:
            for L in range(self.D):
                if (randV() < self.CR or L == self.D-1):
                    tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        return tmp
    
    cdef void report(self):
        """
        report current generation status
        """
        self.timeE = time()
        self.fitnessTime.append((self.gen, self.lastgenbest.f, self.timeE - self.timeS))
    
    cdef bool overbound(self, Chromosome member):
        """
        check the member's chromosome that is out of bound?
        """
        cdef int i
        for i in range(self.D):
            if member.v[i] > self.ub[i] or member.v[i] < self.lb[i]:
                return True
        return False
    
    cdef void generation_process(self):
        cdef int i
        cdef Chromosome tmp
        for i in range(self.NP):
            # generate new vector
            self.generateRandomVector(i)
            # use the vector recombine the member to temporary
            tmp = self.recombination(i)
            # check the one is out of bound?
            if self.overbound(tmp):
                # if it is, then abandon it
                continue
            # is not out of bound, that mean it's quilify of enviorment
            # then evalute the one
            tmp.f = self.evalute(tmp)
            # if temporary one is better than origin(fitness value is smaller)
            if tmp.f <= self.pop[i].f:
                # copy the temporary one to origin member
                self.pop[i].assign(tmp)
                # check the temporary one is better than the currentbest
                if tmp.f < self.currentbest.f:
                    # copy the temporary one to currentbest
                    self.currentbest.assign(tmp)
        # copy the currentbest to lastgenbest
        self.lastgenbest.assign(self.currentbest)
        # if report generation is set, report
        if self.rpt != 0:
            if self.gen % self.rpt == 0:
                self.report()
        else:
            if self.gen % 10 == 0:
                self.report()
    
    cpdef tuple run(self):
        """
        run the algorithm...
        """
        cdef Chromosome tmp
        cdef int i
        # init the member's chromsome
        self.init()
        # find the best one(smallest fitness value)
        tmp = self.findBest()
        # copy to lastgenbest
        self.lastgenbest.assign(tmp)
        # copy to currentbest
        self.currentbest.assign(tmp)
        # report status
        self.report()
        # end initial step
        # the evolution journey is beggin...
        while True:
            self.gen += 1
            if self.option == maxGen:
                if (self.maxGen > 0) and (self.gen > self.maxGen):
                    break
            elif self.option == minFit:
                if self.lastgenbest.f <= self.minFit:
                    break
            elif self.option == maxTime:
                if (self.maxTime > 0) and (time() - self.timeS >= self.maxTime):
                    break
            self.generation_process()
            #progress
            if self.progress_fun is not None:
                self.progress_fun(self.gen, "{:.04f}".format(self.lastgenbest.f))
            #interrupt
            if self.interrupt_fun is not None:
                if self.interrupt_fun():
                    break
        # the evolution journey is done, report the final status
        self.report()
        return self.func.get_coordinates(self.lastgenbest.v), self.fitnessTime
