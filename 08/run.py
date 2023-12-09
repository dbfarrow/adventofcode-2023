#!/usr/bin/env python3
import sys
sys.path.append('..')

import math
import re

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=8) # <----- fill in day here

    def get_input(self):

        lines = [ l for l in super().get_input() if len(l) == 0 or l[0] != '#' ]
        nodes = {}

        for l in lines[2:]:
            m = re.search(r'(.*) = \((.*), (.*)\)', l)
            nodes[m.group(1)] = { 'L': m.group(2), 'R': m.group(3) }

        return lines[0], nodes

    def A(self):
       
        answer = 0
        dirs, nodes = self.get_input()

        answer = 0
        pos = 'AAA'
        while(pos != 'ZZZ'):
            for d in dirs:
#               log.info(f'd={d}, pos={pos}')
                answer += 1
                pos = nodes[pos][d] 
                if pos == 'ZZZ':
                    break

        if self.cmdline.testing:
            expected = 2
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def steps_to_end(self, pos, dirs, nodes):

        steps = 0
        while(pos[-1] != 'Z'):
            d = dirs[steps % len(dirs)]
            pos = nodes[pos][d]
            steps += 1
        return steps

    def B(self):
        
        dirs, nodes = self.get_input()
        pos = [n for n in nodes.keys() if n[-1] == 'A' ]
        answer = 0

        steps = [ self.steps_to_end(p, dirs, nodes) for p in pos ]
        log.info(steps)
        answer = math.lcm(*steps)

        if self.cmdline.testing:
            expected = 6
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer

    def Bduh(self):
        
        dirs, nodes = self.get_input()
        pos = [n for n in nodes.keys() if n[-1] == 'A' ]
        answer = 0

        while True:
            d = dirs[answer % len(dirs)]
            nextp = [ nodes[pos[i]][d] for i in range(len(pos)) ]
            zs = [ True if p[-1] == 'Z' else False for p in pos ]
#           log.info(f'step={answer}, pos={pos} turn {d} to nextp={nextp}, zs={sum(zs)}')
            if sum(zs) > 2:
                log.info(f'step:{answer}, zs={sum(zs)}')
                break
            answer += 1 
            pos = nextp 
            if all(zs):
                break

        if self.cmdline.testing:
            expected = 6
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
