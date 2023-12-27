#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=10) 

    def get_input(self):
        
        data = super().get_input()
        return [ list(l) for l in data if l[0] != '#' ]
        
    def find_start(self, mapp):
    
        # locate the S on the map
        start = None
        for y, l in enumerate(mapp):
            try:
                x = l.index('S')
                start = (x, y)
                break
            except:
                # keep looking
                continue

        if start == None:
            raise Exception('starting point not found')


        # determine which type of pipe section is in that space
        x = start[0]
        y = start[1]
        above = below = left = right = None
        if y > 0 and mapp[y-1][x] in '|F7':                 # above
            above = mapp[y-1][x]
        if y <= len(mapp) - 2 and mapp[y+1][x] in '|LJ':     # below
            below = mapp[y+1][x]
        if x > 0 and mapp[y][x-1] in 'F-L':                 #left
            left = mapp[y][x-1]
        if x <= len(mapp[0]) - 2 and mapp[y][x+1] in '7-J':  #right
            right = mapp[y][x+1]
 
        # using the neighbors that are set, determine the pipe section
        # under the starting point
        pipe = None
        if above and below: pipe = '|'
        elif above and left: pipe = 'J'
        elif above and right: pipe = 'L'
        elif below and left: pipe = '7'
        elif below and right: pipe = 'F'
        elif left and right: pipe = '-'
        else:
            raise Exception(f'cannot determine starting pipe section: left={left}, above={above}, right={right}, below={below}')

#       log.info(f'starting pipe section: left={left}, above={above}, right={right}, below={below}')
        log.info(f'starting pipe section at {start} is a {pipe}')

        # set the pipe section in the map
        mapp[start[1]][start[0]] = pipe

        # select the next step from the top options available. it doesn't matter which way
        # you go
        nextt = None
        if above: nextt = (x, y-1)
        elif right: nextt = (x+1, y)
        elif below: nextt = (x, y+1)
        elif left: nextt = (x-1, y)
        assert nextt != None, f'No next step found'

        return start, nextt

    def print_map(self, mapp):

#       return
        log.info(' ')
        for y in mapp:
            l = ''
            for x in y:
                l += f'{str(x)}' if x != None else '.'
            log.info(l)
        log.info(' ')

    def move(self, p, c, mapp):

        pipe = mapp[c[1]][c[0]]

        x = c[0]
        y = c[1]
        pipe = mapp[y][x]

        nexts = []
        if pipe in '|LJ':                                       # above
            if y > 0: nexts.append((x, y-1))
        if pipe in '|F7':                                       # below
            if y <= len(mapp) - 2: nexts.append((x, y+1))
        if pipe in '-7J':                                       # left
            if x > 0: nexts.append((x-1, y))
        if pipe in 'F-L':                                       # right
            if x <= len(mapp[0]) - 2: nexts.append((x+1, y))

        nexts = [ n for n in nexts if n != p ]
        assert len(nexts) == 1, f'next not found for p={p}, c={c}, pipe:{pipe}: {nexts}, x={len(mapp[0])}'
        return nexts[0]


    def travel_circuit(self, imap):

        smap = [ [ None for i in range(len(imap[0])) ] for i in range(len(imap)) ]

        # when we find the intial node we have to infer the type of pipe section
        # in that space and choosed a direction to move from. we calculate both
        # in find_start() which returns the start node as the "previous" node (p)
        # and the first move which we will call "current" (c)
        step = 1
        c, n = self.find_start(imap)        # previous and current nodes
        smap[c[1]][c[0]] = imap[c[1]][c[0]]

        if self.cmdline.testing:
            self.print_map(imap)
#       log.info(f'step: {step}: {c} ({imap[c[1]][c[0]]})-> {n} ({imap[n[1]][n[0]]})')
        start = c                           # keep track of the starting note
        p = c
        c = n
        step += 1
        vertices = [ start, c ]

        while True:

            # mark our place
            smap[c[1]][c[0]] = imap[c[1]][c[0]]

            # find the next step
            n = self.move(p, c, imap)
#           log.info(f'step: {step}: {c} ({imap[c[1]][c[0]]})-> {n} ({imap[n[1]][n[0]]})')
            p = c
            c = n  
            if c == start: break
            step += 1

            pipe = imap[c[1]][c[0]]
            if pipe in 'LJ7F': vertices.append(c)

        vertices.append(vertices[0])
        return step, smap, vertices

    def A(self):
       
        imap = self.get_input()
        step, smap, vertices = self.travel_circuit(imap)

        answer = step / 2
        if self.cmdline.testing:
            self.print_map(smap)
            expected = 8
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def calc_area(self, steps, points):

        # shoelace algorithm to determine the area of the polygon, including
        # the edges
        A = 0
        for i in range(len(points)-1):
            A += (points[i][1] + points[i+1][1]) * (points[i][0] - points[i+1][0])
#           log.info(f'pn: {points[i]}, pn+1: {points[i+1]}, xp1: {xp1}, xp2:{xp2}, A: {A}')
        A = int(A/2)
        log.info(f'A: {A}')
        return A

    def B(self):
        
        imap = self.get_input()
        steps, smap, points = self.travel_circuit(imap)

        # reverse the steps so they are ordered counter clockwise or we'll 
        # get a negative result
        A = self.calc_area(steps, points)
        if A < 0:
            points.reverse()
            A = self.calc_area(steps, points)

        # count the number of squares on the edge
        b = steps
        log.info(f'b: {b}')
        
        # Pick's theorem says A = i + b/2 - 1 
        # where A is the area of the polygon, i is the number of interior vertices, and
        # b is the number of edge vertices. We need i. A was calculated above
        # using the shoestring theorem
        #
        # i = A - b/2 + 1
        i = A - int(b/2) + 1
        log.info(f'i: {i}')

        answer = i
        if self.cmdline.testing:
            expected = 8
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
