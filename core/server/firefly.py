import random
import math

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

    def __init__(self, D, n, alpha, betaMin, beta0, gamma, lb, ub, f, maxGen, report):
        """
        init the fireflies pool and dimension
        int D, dimension of question
        int n, population
        float alpha
        float betaMin
        float beta0
        flaot gamma
        list of float lb
        list of float ub
        function object f
        int maxGen
        int report
        """
        # D, the dimension of question
        # and each firefly will random place position in this landscape
        self.D = D
        # n, the population size of fireflies
        self.n = n
        # alpha, the step size
        self.alpha = alpha
        # alpha0, use to calculate_new_alpha
        self.alpha0 = alpha
        # betamin, the minimum attration, must not less than this
        self.betaMin = betaMin
        # beta0, the attration of two firefly in 0 distance
        self.beta0 = beta0
        # gamma
        self.gamma = gamma
        # low bound
        self.lb = lb
        # up bound
        self.ub = ub
        # fireflies pool, depend on population n
        self.fireflys = [Chromosome(self.D) for i in range(self.n)]
        # object function, maybe can call the environment
        self.f = f
        # maxima generation
        self.maxGen = maxGen
        # report, how many generation report status once
        self.rp = report
        # generation of current
        self.gen = 0
        # best firefly of geneation
        self.genbest = Chromosome(self.D)
        # best firefly so far
        self.bestFirefly = Chromosome(self.D)

    def init(self):
        """
        init all firefly, each firefly random place in landscape
        """
        for i in range(self.n):
            # init the Chromosome
            for j in range(self.D):
                self.fireflys[i].v[j]=random.random()*(self.ub[j]-self.lb[j])+self.lb[j];

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
        # for i in range(self.n):
        #     self.fireflys[i].f = self.f(self.fireflys[i].v)
        for firefly in self.fireflys:
            firefly.f = self.f(firefly.v)

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
        if self.gen == 0:
            print("Firefly results - init pop")
        elif self.gen == self.maxGen:
            print("Final Firefly results at", self.gen, "generations")
        else:
            print("Final Firefly results after", self.gen, "generations")
        print("Function : %.6f" % (self.bestFirefly.f))
        for i, v in enumerate(self.bestFirefly.v, start=1):
            print("Var", i, ":", v)
        # print("now the gen best fitness is :", self.genbest.f)
        # print("now alpha is :", self.alpha)

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

    def run(self):
        """
        run the algorithm...
        """
        self.init()
        self.evaluate()
        # get one firefly to bestFirefly
        self.bestFirefly.assign(self.fireflys[0])
        self.report()
        for self.gen in range(1, self.maxGen + 1):
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
        # finish all process, report final status
        self.report()
