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

from itertools import product

class NumberSynthesis:
    def __init__(self, NL, NJ):
        self.NL = NL
        self.NJ = NJ
    
    @property
    def Mmax(self):
        if self.NL <= self.NJ and self.NJ <= (2*self.NL-3):
            return self.NJ - self.NL + 2
        elif self.NL == self.NJ and self.NJ == 0:
            raise ValueError("incorrect mechanism.")
        elif (2*self.NL-3) <= self.NJ and self.NJ <= (self.NL*(self.NL-1)/2):
            return self.NL - 1
        else:
            raise ValueError("incorrect mechanism.")
    
    @property
    def NLm(self):
        result = []
        correction = lambda l: sum((i+2)*l[i] for i in range(len(l))) == 2*self.NJ
        Mmax = self.Mmax
        for symbols in product(range(self.NL+1), repeat=Mmax-2):
            NLMmax = self.NL - sum(symbols)
            if NLMmax < 0:
                continue
            answer = symbols+(NLMmax,)
            if correction(answer):
                result.append(answer)
        return tuple(result)
