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

import zmq, time, random, math

class Chromosome(object):
    """
    just copy the idea of genetic algorithm, pretty similar..
    refer to real-coded genetic algorithm(RGA)
    it's call gene in GA, it's call position of dimension in FA
    """
    def __init__(self, n):
        """
        int n, dimension of question
        """
        # dimension
        self.n = n
        self.v = [0] * n
        # the fitness value
        self.f = 0
    
    def distance(self, obj):
        """
        Chromosome obj
        return float
        calculate distance between itself and obj
        """
        dist = 0
        for i in range(self.n):
            dist += (self.v[i] - obj.v[i])**2
        return math.sqrt(dist)
    
    def assign(self, obj):
        """
        Chromosome obj
        copy all attribute from obj to itself
        """
        self.n = obj.n
        self.v = obj.v[:]
        self.f = obj.f

class Firefly(object):
    def __init__(self, func, settings, progress_fun=None, interrupt_fun=None):
        # D, the dimension of question
        # and each firefly will random place position in this landscape
        self.D = settings['nParm']
        # n, the population size of fireflies
        self.n = settings['n']
        # alpha, the step size
        self.alpha = settings['alpha']
        # alpha0, use to calculate_new_alpha
        self.alpha0 = settings['alpha']
        # betamin, the minimum attration, must not less than this
        self.betaMin = settings['betaMin']
        # beta0, the attration of two firefly in 0 distance
        self.beta0 = settings['beta0']
        # gamma
        self.gamma = settings['gamma']
        # low bound
        self.lb = settings['lower']
        # up bound
        self.ub = settings['upper']
        # fireflies pool, depend on population n
        self.fireflys = [Chromosome(self.D) for i in range(self.n)]
        # object function, maybe can call the environment
        self.func = func
        # maxima generation, report: how many generation report status once
        self.maxGen = settings['maxGen']
        self.rp = settings['report']
        self.progress_fun = progress_fun
        self.interrupt_fun = interrupt_fun
        # generation of current
        self.gen = 0
        # best firefly of geneation
        self.genbest = Chromosome(self.D)
        # best firefly so far
        self.bestFirefly = Chromosome(self.D)
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
    
    def init(self):
        """
        init all firefly, each firefly random place in landscape
        """
        for i in range(self.n):
            # init the Chromosome
            for j in range(self.D):
                self.fireflys[i].v[j]=random.random()*(self.ub[j]-self.lb[j])+self.lb[j]
    
    def movefireflies(self):
        """
        move fireflies, this is most import step of whole algorithm
        firefly will check each another firefly that light intensity is stronger than itself
        if anyone is better than itself, the firefly will toward to her with alpha, gamma, betaMin, beta and r affect
        if not, then randomly move
        
        above step also need to check the bound
        
        note:
        
        1. light intensity = 1 / fitness value, lower fitness value represent better light intensity
        2. scale mean the landscape range in dimension e.g. 50 to -50 then scale will be 100
        """
        for i in range(self.n):
            is_move = False
            for j in range(self.n):
                # check is any one firefly is better any itself
                is_move |= self.movefly(self.fireflys[i], self.fireflys[j])
            # if not, then randomly move
            if not is_move:
                for k in range(self.D):
                    scale = self.ub[k] - self.lb[k]
                    self.fireflys[i].v[k] += self.alpha * (random.random() - 0.5) * scale
                    # check bound
                    self.fireflys[i].v[k] = self.check(k, self.fireflys[i].v[k])
    
    def evaluate(self):
        """
        evaluate each firefly's fitness value
        """
        for firefly in self.fireflys:
            #firefly.f = self.func(firefly.v)
            firefly.f = self.socket_fitness(firefly.v)
    
    def movefly(self, me, she):
        """
        Chromosome object me, she
        return bool, am i move?
        
        two firefly me, she
        Is my fitness value larger than her,
        if it is true, then toward to her, need to check the dimension bound
        
        note: fitness value low is better
        """
        # is my fitness value larger than her
        if me.f > she.f:
            # calculate the distance between me and her
            r = me.distance(she)
            # beta = self.beta0 * math.exp(-self.gamma * (r**2))
            # beta = self.betaMin if beta < self.betaMin else beta
            beta = (self.beta0-self.betaMin)*math.exp(-self.gamma*(r**2))+self.betaMin
            for i in range(me.n):
                scale = self.ub[i] - self.lb[i]
                me.v[i] += beta * (she.v[i] - me.v[i]) + self.alpha*(random.random()-0.5) * scale
                me.v[i] = self.check(i, me.v[i])
            return True
        return False
    
    def check(self, i, v):
        """
        int i, float v
        return a float value

        check the value v is in the i dimension bound
        if it is inside the bound, just return the value v
        if v is larger than bound of upper, return bound of upper value
        if v is lower than bound of lower, return bound of lower value
        """
        # if v > self.ub[i] or v < self.lb[i]:
        #     return self.randVal(self.lb[i], self.ub[i])
        # return v
        if v > self.ub[i]:
            return self.ub[i]
        elif v < self.lb[i]:
            return self.lb[i]
        else:
            return v
    
    def randVal(self, low, high):
        """
        float low, high
        return float
        """
        return random.random()*(high-low)+low
    
    def findFirefly(self):
        """
        return Chromosome object
        find the best one firefly(minimum fitness value) in fireflys
        """
        return min(self.fireflys, key=lambda chrom:chrom.f)
    
    def report(self):
        """
        report current generation status
        """
        self.timeE = time.time()
        self.fitnessTime += '%d,%.3f,%d;'%(self.gen, self.bestFirefly.f, self.timeE - self.timeS)
    
    def calculate_new_alpha(self):
        """
        calculate new alpha, why need this?
        in larger fitness value step, it need larger alpha(move quick to convergence)
        but in smaller fitness value step, it need smaller alpha
        (move slow, this step is pretty close the answer that we want)
        """
        # self.alpha = self.alpha0 / math.log(self.gen + 1)
        # depend on cureent gen best firefly
        self.alpha = self.alpha0 * math.log10(self.genbest.f + 1)
    
    def getParamValue(self):
        self.fitnessParameter = ','.join(['%.4f'%(v) for v in self.bestFirefly.v])
    
    def generation_process(self):
        self.movefireflies()
        self.evaluate()
        # adjust alpha, depend on fitness value
        # if fitness value is larger, then alpha should larger
        # if fitness value is small, then alpha should smaller
        self.genbest.assign(self.findFirefly())
        # if the best firefly of this generation is better than
        # bestFirefly, copy all its
        if self.bestFirefly.f > self.genbest.f:
            self.bestFirefly.assign(self.genbest)
        # generate new alpha
        self.calculate_new_alpha()
        # report?
        if self.rp != 0:
            if self.gen % self.rp == 0:
                self.report()
        if self.progress_fun is not None:
            self.progress_fun(self.gen, '%.4f'%self.bestFirefly.f)
    
    def run(self):
        """
        run the algorithm...
        """
        self.init()
        self.evaluate()
        # get one firefly to bestFirefly
        self.bestFirefly.assign(self.fireflys[0])
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
        # finish all process, report final status
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
