#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
import re

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=18)

    def get_input(self):
    
        data = super().get_input()
        plan = []
        for l in data:
            m = re.match('([LRUD]) ([0-9]+) (.*)', l)
            if m: plan.append((m.group(1), int(m.group(2)), m.group(3)))    
        return plan

    def calc_capacity(self, plan):
        
        points = [ (0, 0) ]
        for p in plan:
            (d, n, c) = p
            prev = points[-1]
            if d == 'R': points.append((prev[0]+n, prev[1]))
            if d == 'L': points.append((prev[0]-n, prev[1]))
            if d == 'U': points.append((prev[0], prev[1]-n))
            if d == 'D': points.append((prev[0], prev[1]+n))

        # shoelace algorithm to determine the area of the polygon, including
        # the edges
        A = 0
        for i in range(len(points)-1):
            xp1 = (points[i][0] * points[i+1][1])   # xn * yn+1
            xp2 = (points[i+1][0] * points[i][1])   # xn+1 * yn
            A += (xp1 - xp2)
#           log.info(f'pn: {points[i]}, pn+1: {points[i+1]}, xp1: {xp1}, xp2:{xp2}, A: {A}')
        A = int(A/2)
        log.info(f'A: {A}')

        # count the number of squares on the edge
        b = sum( [ p[1] for p in plan ])
        log.info(f'b: {b}')
        
        # Pick's theorem says A = i + b/2 - 1 
        # where A is the area of the polygon, i is the number of interior vertices, and
        # b is the number of edge vertices. We need i. A was calculated above
        # using the shoestring theorem
        #
        # i = A - b/2 + 1
        i = A - int(b/2) + 1
        log.info(f'i: {i}')

        return b + i
         
    def A(self):
        plan = self.get_input()
        answer = self.calc_capacity(plan) 
        if self.cmdline.testing:
            expected = 62
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer

    def B(self):
       
        dirs = 'RDLU'
        plan = [ (dirs[int(p[2][7])], int(p[2][2:7], 16), p[2]) for p in self.get_input() ]
        answer = self.calc_capacity(plan) 

        if self.cmdline.testing:
            expected = 952408144115
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer



if __name__ == "__main__":
    AOC().run()
