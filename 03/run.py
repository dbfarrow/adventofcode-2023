#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=3) 

    def get_input(self):
       
        parts = []
        symbols = []
        lines = super().get_input()
        
        part = ''
        startx = starty = None
        for y, l in enumerate(lines):
            for x, c in enumerate(l):
                if c.isdigit():
                    if startx == None:
                        startx = x
                        starty = y
                    part = f'{part}{c}'
                else:
                    if len(part) > 0:
                        parts.append([ int(part), (startx, starty), (x-1, y) ])
                        part = ''
                        startx = starty = None
                    if c != '.':
                        symbols.append([ c, (x, y) ])

            if len(part) > 0:
                parts.append([ int(part), (startx, starty), (x, y) ])
                part = ''
                startx = starty = None

        return parts, symbols

    def A(self):

        answer = 0
        (parts, symbols) = self.get_input()

        realparts = []
        for part in parts:
            ss = [ sym for sym in symbols 
                    if sym[1][1] >= part[1][1]-1            # starty - 1
                        and sym[1][1] <= part[2][1]+1       # endy + 1
                        and sym[1][0] >= part[1][0]-1       # startx - 1
                        and sym[1][0] <= part[2][0]+1 ]     # enx + 1
            if any(ss):
                realparts.append(part[0]) 
#           else:
#               log.info(f'part: {part} is not a real part number')

        answer = sum(realparts)
        if self.cmdline.testing:
            assert answer == 4361, f'expected 4361, got {answer}'
        return answer

    def B(self):

        answer = 0
        (parts, symbols) = self.get_input()

        gears = [s for s in symbols if s[0] == '*' ]
        ratios = []
        for gear in gears:
            neighbors = [ part for part in parts 
                    if gear[1][1] >= part[1][1]-1            # starty - 1
                        and gear[1][1] <= part[2][1]+1       # endy + 1
                        and gear[1][0] >= part[1][0]-1       # startx - 1
                        and gear[1][0] <= part[2][0]+1 ]     # enx + 1
            if len(neighbors) == 2:
                ratios.append(neighbors[0][0] * neighbors[1][0])

        answer = sum(ratios)

        if self.cmdline.testing:
            assert answer == 467835, f'expected 467835, got {answer}'
        return answer

if __name__ == "__main__":
    AOC().run()
