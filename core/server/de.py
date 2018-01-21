# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
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

import zmq, time, random

class Chromosome(object):
    """
    just copy the idea of genetic algorithm, pretty similar..
    """
    def __init__(self, n):
        """
        int n, dimension of question
        """
        # dimension
        self.n = n
        # the gene
        self.v = [0] * n
        # the fitness value
        self.f = 0
    
    def assign(self, obj):
        """
        Chromosome obj
        copy all attribute from obj to itself
        """
        self.n = obj.n
        self.v = obj.v[:]
        self.f = obj.f

class DiffertialEvolution(object):
    def __init__(self, func, settings, socket_port, progress_fun=None, interrupt_fun=None):
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
        # lower bound array
        self.lb = self.func.get_lower()
        # upper bound array
        self.ub = self.func.get_upper()
        # maxima generation, report: how many generation report status once
        self.maxGen = settings['maxGen']
        self.rpt = settings['report']
        self.progress_fun = progress_fun
        self.interrupt_fun = interrupt_fun
        # check parameter is set properly
        self.checkParameter()
        # generation pool, depend on population size
        self.pop = [Chromosome(self.D) for i in range(self.NP)]
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
        #socket
        self.socket_port = settings['socket_port']
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.bind(self.socket_port)
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)
        self.targetPath = settings['Target']
        # setup benchmark
        self.timeS = time.time()
        self.timeE = 0
        self.fitnessTime = ''
        self.fitnessParameter = ''
    
    def checkParameter(self):
        """
        check parameter is set properly
        """
        if (type(self.D) is not int) and self.D <= 0:
            raise Exception('D shoud be integer and larger than 0')
        if (type(self.NP) is not int) and self.NP <= 0:
            raise Exception('NP shoud be integer and larger than 0')
        if self.CR < 0 or self.CR > 1:
            raise Exception('CR should be [0,1]')
        if self.maxGen < 0:
            raise Exception('generation should larger than 0')
        if self.rpt <= 0 or self.rpt > self.maxGen:
            raise Exception('report should be larger than 0 and less than max genration')
        if self.strategy < 1 or self.strategy > 10:
            raise Exception('strategy should be [1,10]')
        for lower, upper in zip(self.lb, self.ub):
            if lower > upper:
                raise Exception('upper bound should be larger than lower bound')
    
    def init(self):
        """
        init population
        """
        for i in range(self.NP):
            for j in range(self.D):
                self.pop[i].v[j] = self.lb[j] + random.random()*(self.ub[j] - self.lb[j])
            self.pop[i].f = self.evalute(self.pop[i])
    
    def evalute(self, p):
        """
        evalute the member in enviorment
        """
        #return self.func(p.v)
        return self.socket_fitness(p.v)
    
    def findBest(self):
        """
        find member that have minimum fitness value from pool
        """
        return min(self.pop, key=lambda chrom:chrom.f)
    
    def generateRandomVector(self, i):
        """
        generate new vector
        """
        while True:
            self.r1 = int(random.random() * self.NP)
            if not (self.r1 == i):
                break
        while True:
            self.r2 = int(random.random() * self.NP)
            if not ((self.r2 == i) or (self.r2 == self.r1)):
                break
        while True:
            self.r3 = int(random.random() * self.NP)
            if not ((self.r3 == i) or (self.r3 == self.r1) or (self.r3 == self.r2)):
                break
        while True:
            self.r4 = int(random.random() * self.NP)
            if not ((self.r4 == i) or (self.r4 == self.r1) or (self.r4 == self.r2) or (self.r4 == self.r3)):
                break
        while True:
            self.r5 = int(random.random() * self.NP)
            if not ((self.r5 == i) or (self.r5 == self.r1) or (self.r5 == self.r2) or (self.r5 == self.r3) or (self.r5 == self.r4)):
                break
    
    def recombination(self, i):
        """
        use new vector, recombination the new one member to tmp
        """
        tmp = Chromosome(self.D)
        if self.strategy==1:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((random.random() < self.CR) and (L < self.D)):
                    break
        elif self.strategy==2:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((random.random() < self.CR) and (L < self.D)):
                    break
        elif self.strategy==3:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            L = 0
            while True:
                tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
                L += 1
                if not ((random.random() < self.CR) and (L < self.D)):
                    break
        elif self.strategy==4:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not ((random.random() < self.CR) and (L < self.D)):
                    break
        elif self.strategy==5:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            L = 0
            while True:
                tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
                L += 1
                if not ((random.random() < self.CR) and (L < self.D)):
                    break
        elif self.strategy==6:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            for L in range(self.D):
                if ((random.random() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.lastgenbest.v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif self.strategy==7:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            for L in range(self.D):
                if ((random.random() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.pop[self.r1].v[n] + self.F*(self.pop[self.r2].v[n] - self.pop[self.r3].v[n])
                n = (n + 1) % self.D
        elif self.strategy==8:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            for L in range(self.D):
                if ((random.random() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = tmp.v[n] + self.F*(self.lastgenbest.v[n] - tmp.v[n]) + self.F*(self.pop[self.r1].v[n] - self.pop[self.r2].v[n])
                n = (n + 1) % self.D
        elif self.strategy==9:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            for L in range(self.D):
                if ((random.random() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.lastgenbest.v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        else:
            tmp.assign(self.pop[i])
            n = int(random.random() * self.D)
            for L in range(self.D):
                if ((random.random() < self.CR) or L == (self.D - 1)):
                    tmp.v[n] = self.pop[self.r5].v[n] + (self.pop[self.r1].v[n] + self.pop[self.r2].v[n] - self.pop[self.r3].v[n] - self.pop[self.r4].v[n]) * self.F
                n = (n + 1) % self.D
        return tmp
    
    def report(self):
        """
        report current generation status
        """
        self.timeE = time.time()
        self.fitnessTime += '%d,%.3f,%d;'%(self.gen, self.lastgenbest.f, self.timeE - self.timeS)
    
    def overbound(self, member):
        """
        check the member's chromosome that is out of bound?
        """
        for i in range(self.D):
            if member.v[i] > self.ub[i] or member.v[i] < self.lb[i]:
                return True
        return False
    
    def getParamValue(self):
        self.fitnessParameter = ','.join(['%.4f'%(v) for v in self.lastgenbest.v])
    
    def generation_process(self):
        for i in range(self.NP):
            # generate new vector
            self.generateRandomVector(i)
            # use the vector recombine the member to temporary
            tmp = self.recombination(i)
            # check the one is out of bound?
            if self.overbound(tmp):
                # if it is, then ignore
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
        if self.progress_fun is not None:
            self.progress_fun(self.gen, '%.4f'%self.lastgenbest.f)
    
    def run(self):
        """
        run the algorithm...
        """
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
        # the evolution journey is done, report the final status
        self.report()
        self.getParamValue()
        self.context.term()
        return self.fitnessTime, self.fitnessParameter
    
    def socket_fitness(self, chrom):
        if self.socket.closed:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.bind(self.socket_port)
            self.poll.register(self.socket, zmq.POLLIN)
        self.socket.send_string(';'.join([
            self.func.get_Driver(),
            self.func.get_Follower(),
            self.func.get_Link(),
            self.func.get_Target(),
            self.func.get_ExpressionName(),
            self.func.get_Expression(),
            str(self.targetPath),
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
