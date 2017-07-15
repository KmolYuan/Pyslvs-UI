# -*- coding: utf-8 -*-
from cpython cimport bool
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, RAND_MAX, srand
from libc.time cimport time

# make true it is random everytime
srand(time(NULL))

cdef double randV():
    return rand()/(RAND_MAX*1.0)

cdef class Chromosome(object):
    """
    just copy the idea of genetic algorithm, pretty similar..
    """
    cdef public int n
    cdef public double f
    cdef public np.ndarray v
    
    def __cinit__(self, int n):
        """
        int n, dimension of question
        """
        # dimension
        self.n = n
        # the gene
        self.v = np.zeros(n)
        # the fitness value
        self.f = 0
    
    def assign(self, Chromosome obj):
        """
        Chromosome obj
        copy all attribute from obj to itself
        """
        self.n = obj.n
        self.v[:] = obj.v
        self.f = obj.f

cdef class DiffertialEvolution(object):
    cdef:
        int strategy, D, NP, maxGen, rpt, gen, r1, r2, r3, r4, r5
        double F, CR
        np.ndarray lb, ub, pop
        object f
        Chromosome lastgenbest, currentbest
    cdef int timeS, timeE
    cdef object fitnessTime, fitnessParameter
    
    def __cinit__(self, object Func, int strategy, int D, int NP, double F, double CR,
            object lower, object upper, int maxGen, int report):
        # strategy 1~10, choice what strategy to generate new member in temporary
        self.strategy = strategy
        # dimesion of quesiton
        self.D = D
        # population size
        # To start off NP = 10*D is a reasonable choice. Increase NP if misconvergence
        self.NP = NP
        # weight factor
        # F is usually between 0.5 and 1 (in rare cases > 1)
        self.F = F
        # crossover possible
        # CR in [0,1]
        self.CR = CR
        # low bound
        self.lb = np.array(lower[:])
        # up bound
        self.ub = np.array(upper[:])
        # maximum generation
        self.maxGen = maxGen
        # how many generation report once
        self.rpt = report
        # object function, or enviorment
        self.f = Func
        # check parameter is set properly
        self.checkParameter()
        
        # generation pool, depend on population size
        self.pop = np.ndarray((NP,),dtype=np.object)
        for i in range(NP):
            self.pop[i] = Chromosome(self.D)
        # last generation best member
        self.lastgenbest = Chromosome(D)
        # current best member
        self.currentbest = Chromosome(D)
        # the generation count
        self.gen = 0
        # the vector
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        self.r5 = 0
        
        # setup benchmark
        self.timeS = time(NULL)
        self.timeE = 0
        self.fitnessTime = ''
        self.fitnessParameter = ''
    
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
        if self.maxGen <= 0:
            raise Exception('generation should larger than 0')
        if self.rpt <= 0 or self.rpt > self.maxGen:
            raise Exception('report should be larger than 0 and less than max genration')
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
        return self.f(member.v)
    
    cdef Chromosome findBest(self):
        """
        find member that have minimum fitness value from pool
        """
        return min(self.pop, key=lambda chrom:chrom.f)
    
    cdef void generateRandomVector(self, i):
        """
        generate new vector
        """
        while True:
            self.r1 = int(randV() * self.NP)
            if not (self.r1 == i):
                break
        while True:
            self.r2 = int(randV() * self.NP)
            if not ((self.r2 == i) or (self.r2 == self.r1)):
                break
        while True:
            self.r3 = int(randV() * self.NP)
            if not ((self.r3 == i) or (self.r3 == self.r1) or (self.r3 == self.r2)):
                break
        while True:
            self.r4 = int(randV() * self.NP)
            if not ((self.r4 == i) or (self.r4 == self.r1) or (self.r4 == self.r2) or (self.r4 == self.r3)):
                break
        while True:
            self.r5 = int(randV() * self.NP)
            if not ((self.r5 == i) or (self.r5 == self.r1) or (self.r5 == self.r2) or (self.r5 == self.r3) or (self.r5 == self.r4)):
                break
    
    cdef Chromosome recombination(self, int i):
        """
        use new vector, recombination the new one member to tmp
        """
        cdef Chromosome tmp
        cdef int n, L
        tmp = Chromosome(self.D)
        if self.strategy == 1:
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((randV() < self.CR) and (L < self.D)):
                    break
        elif self.strategy == 2:
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((randV() < self.CR) and (L < self.D)):
                    break
        elif (self.strategy == 3):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            L = 0
            while True:
                tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((randV() < self.CR) and (L < self.D)):
                    break
        elif (self.strategy == 4):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not ((randV() < self.CR) and (L < self.D)):
                    break
        elif (self.strategy == 5):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not ((randV() < self.CR) and (L < self.D)):
                    break
        elif (self.strategy == 6):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            for L in range(self.D):
                if ((randV() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif (self.strategy == 7):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            for L in range(self.D):
                if ((randV() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif (self.strategy == 8):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            for L in range(self.D):
                if ((randV() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
        elif (self.strategy == 9):
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            for L in range(self.D):
                if ((randV() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        else:
            tmp.assign(self.pop[i])
            n = int(randV() * self.D)
            for L in range(self.D):
                if ((randV() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        return tmp
    
    cdef void report(self):
        """
        report current generation status
        """
        self.timeE = time(NULL)
        self.fitnessTime += '%d,%.3f,%d;'%(self.gen, self.lastgenbest.f, self.timeE - self.timeS)
    
    cdef bool overbound(self, Chromosome member):
        """
        check the member's chromosome that is out of bound?
        """
        cdef int i
        for i in range(self.D):
            if member.v[i] > self.ub[i] or member.v[i] < self.lb[i]:
                return True
        return False
    
    cdef void getParamValue(self):
        self.fitnessParameter = ','.join(['%.4f'%(v) for v in self.lastgenbest.v])
    
    cpdef run(self):
        """
        run the algorithm...
        """
        cdef Chromosome tmp
        cdef int i
        # initial step
        # generation 0
        self.gen = 0
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
        for self.gen in range(1, self.maxGen + 1):
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
        # the evolution journey is done, report the final status
        self.report()
        self.getParamValue()
        return self.fitnessTime, self.fitnessParameter
