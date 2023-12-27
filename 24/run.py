#!/usr/bin/env python3
import sys
sys.path.append('..')

import itertools 
import re
import sympy as sym
from z3 import Int, Solver

from shared.aoc import __AOC
from shared import log

class Formula():

    def __init__(self, spec):
        
        m = re.match('(.*), (.*), (.*) @ (.*), (.*), (.*)', spec)
        assert m, f'failed to parse spec: {spec}'
        
        self.x = int(m.group(1))
        self.y = int(m.group(2))
        self.z = int(m.group(3))
        self.dx = int(m.group(4))
        self.dy = int(m.group(5))
        self.dz = int(m.group(6))

        # f(x) = y = mx + c
        # c = y - mx
        self.m = self.dy / self.dx
        self.c = self.y - (self.m * self.x)

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z}) -> m={self.m}, c={self.c}'

    def intersects(self, other):
        
        # f1(x) = y1 = m1*x + c1
        # f2(x) = y2 = m2*x + c2
        #
        # f1 and f2 intersect when y1 == y2
        #
        # m1*x + c1 = m2*x + c2
        # m1*x - m2*x = c2 - c1
        # x(m1 - m2) = c2 - c1
        # x = (c2 - c1) / (m1 - m2)
        #
        if self.m - other.m != 0:
            x = (other.c - self.c) / (self.m - other.m)
            y = (self.m * x) + self.c
            afuture = (x > self.x if self.dx >= 0 else x < self.x)
            bfuture = (x > other.x if other.dx >= 0 else x < other.x)
            return (self, other, (x, y), afuture, bfuture)
        else:
            return (self, other, (None, None), None, None)

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=24)

    def get_input(self):
        return [ Formula(l) for l in super().get_input() ]

    def A(self):
       
        bounds = (7, 27) if self.cmdline.testing else (200000000000000, 400000000000000)
        fs = self.get_input()
        log.info(f'bounds: {bounds}')

        inters = [ a.intersects(b) for a, b in itertools.combinations(fs, 2) ]
        answer = 0
        for f1, f2, i, afuture, bfuture in inters:
            if not i[0]: continue
            if (bounds[0] <= i[0] <= bounds[1]) and (bounds[0] <= i[1] <= bounds[1]) and afuture and bfuture:
                answer += 1

        if self.cmdline.testing:
            expected = 2
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    # This solution was shamelessly lifted from the work of hildjj*. I never would have sorted 
    # this on my own. Thanks go to him for pointing me towards z3 as the solution and for
    # a working example from which to learn how z3 works. Both hildjj and z3 are amazing.
    #
    #   *https://github.com/hildjj/AdventOfCode2023/blob/main/day24.py
    #
    def B(self):
        
        s = Solver()
        x = Int('x')
        y = Int('y')
        z = Int('z')
        dx = Int('dx')
        dy = Int('dy')
        dz = Int('dz')

        fs = self.get_input()[0:3]
        for ix, f in enumerate(fs):
            t = Int(f't{ix}')
            s.add((f.x + (f.dx*t)) == (x + (dx*t)))
            s.add((f.y + (f.dy*t)) == (y + (dy*t)))
            s.add((f.z + (f.dz*t)) == (z + (dz*t)))
        log.info(f'check: {s.check()}')

        a = s.model()
        answer = 0
        answer += a[x].as_long()
        answer += a[y].as_long()
        answer += a[z].as_long()

        if self.cmdline.testing:
            expected = 47
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
