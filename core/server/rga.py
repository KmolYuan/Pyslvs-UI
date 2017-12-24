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

import zmq, time, math

class Chromosome(object):
    def __init__(self, n=None):
        self.np = n if n > 0 else 2
        self.f = 0.0
        self.v = [0.0]*n
    
    def cp(self, obj):
        """
        copy all atribute from another chromsome object
        """
        self.np = obj.np
        self.f = obj.f
        self.v = obj.v[:]
    
    def get_v(self, i):
        return self.v[i]
    
    def is_self(self, obj):
        """
        check the object is self?
        """
        return obj is self
    
    def assign(self, obj):
        if not self.is_self(obj):
            self.cp(obj)

class Genetic(object):
    def __init__(self, func, settings, progress_fun=None, interrupt_fun=None):
        self.func = func
        self.nParm = settings['nParm']
        self.nPop = settings['nPop']
        self.pCross = settings['pCross']
        self.pMute = settings['pMute']
        self.pWin = settings['pWin']
        self.bDelta = settings['bDelta']
        
        self.chrom = [Chromosome(self.nParm) for i in range(self.nPop)]
        self.newChrom = [Chromosome(self.nParm) for i in range(self.nPop)]
        self.babyChrom = [Chromosome(self.nParm) for i in range(3)]
        self.chromElite = Chromosome(self.nParm)
        self.chromBest = Chromosome(self.nParm)
        self.maxLimit = settings['upper'][:]
        self.minLimit = settings['lower'][:]
        #Gen
        self.maxGen = settings['maxGen']
        self.rpt = settings['report']
        self.progress_fun = progress_fun
        self.interrupt_fun = interrupt_fun
        self.gen = 0
        # setup benchmark
        self.timeS = time.time()
        self.timeE = 0
        self.fitnessTime = ''
        self.fitnessParameter = ''
        #seed
        self.seed = 0.0
        self.iseed = 470211272.0
        self.mask = 2147483647
        #socket
        self.socket_port = settings['socket_port']
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.bind(self.socket_port)
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)
        self.targetPath = settings['targetPath']
        # setup benchmark
        self.timeS = time.time()
        self.timeE = 0
        self.fitnessTime = ''
        self.fitnessParameter = ''
    
    def newSeed(self):
        if self.seed==0.:
            self.seed = self.iseed
        else:
            self.seed *= 16807.0
            self.seed = math.fmod(self.seed, self.mask)
    
    def rnd(self):
        self.newSeed()
        return self.seed/self.mask
    
    def randomize(self):
        self.seed = time.time()
    
    def random(self, k):
        return int(self.rnd()*k)
    
    def randVal(self, low, high):
        number_types = (int, float)
        if isinstance(low, number_types) and isinstance(high, number_types):
            return self.rnd()*(high-low)+low
        raise ValueError
    
    def check(self, i, v):
        """
        If a variable is out of bound,
        replace it with a random value
        """
        if v>self.maxLimit[i] or v<self.minLimit[i]: return self.randVal(self.minLimit[i], self.maxLimit[i])
        return v
    
    def initialPop(self):
        for j in range(self.nPop):
            for i in range(self.nParm):
                self.chrom[j].v[i] = self.randVal(self.minLimit[i], self.maxLimit[i])
    
    def select(self):
        """
        roulette wheel selection
        """
        for i in range(self.nPop):
            j = self.random(self.nPop)
            k = self.random(self.nPop)
            self.newChrom[i].assign(self.chrom[j])
            if self.chrom[k].f<self.chrom[j].f and self.rnd()<self.pWin:
                self.newChrom[i].assign(self.chrom[k])
        # in this stage, newChrom is select finish
        # now replace origin chrom
        for i in range(self.nPop):
            self.chrom[i].assign(self.newChrom[i])

        # select random one chrom to be best chrom, make best chrom still exist
        j = self.random(self.nPop)
        self.chrom[j].assign(self.chromElite)
    
    def crossOver(self):
        for i in range(0, self.nPop-1, 2):
            # crossover
            if(self.rnd() < self.pCross):
                for s in range(self.nParm):
                    # first baby, 1/2 father 1/2 mother
                    self.babyChrom[0].v[s] = 0.5 * self.chrom[i].v[s] + 0.5*self.chrom[i+1].v[s]
                    # second baby, 3/4 of fater and 1/4 of mother
                    self.babyChrom[1].v[s] = self.check(s, 1.5 * self.chrom[i].v[s] - 0.5*self.chrom[i+1].v[s])
                    # third baby, 1/4 of fater and 3/4 of mother
                    self.babyChrom[2].v[s] = self.check(s,-0.5 * self.chrom[i].v[s] + 1.5*self.chrom[i+1].v[s])
                for j in range(3):
                    self.babyChrom[j].f = self.socket_fitness(self.babyChrom[j].v)
                    #self.babyChrom[j].f = self.func(self.babyChrom[j].v)
                
                if self.babyChrom[1].f < self.babyChrom[0].f:
                    self.babyChrom[0], self.babyChrom[1] = self.babyChrom[1], self.babyChrom[0]
                if self.babyChrom[2].f < self.babyChrom[0].f:
                    self.babyChrom[2], self.babyChrom[0] = self.babyChrom[0], self.babyChrom[2]
                if self.babyChrom[2].f < self.babyChrom[1].f:
                    self.babyChrom[2], self.babyChrom[1] = self.babyChrom[1], self.babyChrom[2]
                
                # replace first two baby to parent, another one will be
                self.chrom[i].assign(self.babyChrom[0])
                self.chrom[i+1].assign(self.babyChrom[1])
    
    def mutate(self):
        def delta(y):
            r = float(self.gen) / self.maxGen
            return y*self.rnd()*math.pow(1.0-r, self.bDelta)
        for i in range(self.nPop):
            if self.rnd() < self.pMute:
                s = self.random(self.nParm)
                if (self.random(2) == 0):
                    self.chrom[i].v[s] += delta(self.maxLimit[s]-self.chrom[i].v[s])
                else:
                    self.chrom[i].v[s] -= delta(self.chrom[i].v[s]-self.minLimit[s])
    
    def fitness(self):
        for j in range(self.nPop):
            #Calculate the fitness value
            self.chrom[j].f = self.socket_fitness(self.chrom[j].v)
            #self.chrom[j].f = self.func(self.chrom[j].v)
        self.chromBest.assign(self.chrom[0])
        for j in range(self.nPop):
            if(self.chrom[j].f < self.chromBest.f):
                self.chromBest.assign(self.chrom[j])
        if(self.chromBest.f < self.chromElite.f):
            self.chromElite.assign(self.chromBest)
    
    def report(self):
        self.timeE = time.time()
        self.fitnessTime += '%d,%.3f,%d;'%(self.gen, self.chromElite.f, self.timeE-self.timeS)
    
    def getParamValue(self):
        self.fitnessParameter = ','.join(['%.4f'%(v) for v in self.chromElite.v])
    
    def generation_process(self):
        self.select()
        self.crossOver()
        self.mutate()
        self.fitness()
        if self.rpt != 0:
            if self.gen%self.rpt == 0:
                self.report()
        if self.progress_fun is not None:
            self.progress_fun(self.gen)
    
    def run(self):
        """
        Init and run GA for maxGen times
        mxg : maximum generation
        rp  : report cycle, 0 for final report or report each mxg modulo rp
        """
        self.randomize()
        self.initialPop()
        self.chrom[0].f = self.socket_fitness(self.chrom[0].v)
        self.chromElite.assign(self.chrom[0])
        self.gen = 0
        self.fitness()
        self.report()
        if self.maxGen>0:
            for self.gen in range(1, self.maxGen+1):
                self.generation_process()
                if self.interrupt_fun is not None:
                    if self.interrupt_fun():
                        break
        else:
            while True:
                self.generation_process()
                if self.interrupt_fun is not None:
                    if self.interrupt_fun():
                        break
        self.getParamValue()
        self.context.term()
        return self.fitnessTime, self.fitnessParameter
    
    def socket_fitness(self, chrom):
        if self.socket.closed:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.bind(self.socket_port)
            self.poll.register(self.socket, zmq.POLLIN)
        self.socket.send_string(';'.join([
            self.func.get_Driving(),
            self.func.get_Follower(),
            self.func.get_Link(),
            self.func.get_Target(),
            self.func.get_ExpressionName(),
            self.func.get_Expression(),
            ','.join(["{}:{}".format(e[0], e[1]) for e in self.targetPath]),
            ','.join([str(e) for e in chrom])
            ]))
        while True:
            socks = dict(self.poll.poll(100))
            if socks.get(self.socket)==zmq.POLLIN:
                return float(self.socket.recv().decode('utf-8'))
            else:
                self.socket.setsockopt(zmq.LINGER, 0)
                self.socket.close()
                self.poll.unregister(self.socket)
                return self.func(chrom)
