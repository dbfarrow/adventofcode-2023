#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import Counter, defaultdict
from itertools import groupby

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=14)

    def get_input(self):
        return [ list(l) for l in super().get_input() ]

    
    def tilt_north(self, rocks):
        
        for y in range(1, len(rocks)):
            for x in range(len(rocks[0])):
                if rocks[y][x] == 'O':

                    # start looking at the row above for space to move
                    if y == 0: continue

                    # if there's no space to move, move to the next rock
                    if rocks[y-1][x] != '.': 
#                       log.info(f'({x}, {y}) cannot move')
                        continue

                    # now travel up the column above the rock till we hit another
                    # rock or the top of the map
                    spaces = 0
                    for yy in range(y-1, -1, -1):
                        if rocks[yy][x] == '.': 
                            spaces += 1
                        else:
                            break

                    yy = y - spaces
                    assert yy >= 0, f'calculating yy for rock at ({x},{y}): yy = {yy}'
                    assert rocks[yy][x] == '.', f'({x}, {y}): spaces={spaces}, rocks[{yy}][{x}] = {rocks[yy][x]}'
                    rocks[yy][x] = 'O'
                    rocks[y][x] = '.'
#                   log.info(f'({x}, {y}) moved to ({x}, {yy})') 
        return rocks

    def tilt_west(self, rocks):
        
        X = len(rocks[0])
        Y = len(rocks)

        for y in range(Y):
            for x in range(X):
                if rocks[y][x] == 'O':
        
                    # start looking at the column to the left for space to move
                    if x == 0: continue

                    # if there's no space to move, move to the next rock
                    if rocks[y][x-1] != '.': continue

                    # now travel left on the rock's row till we hit another rock or the 
                    # side of the map
                    spaces = 0
                    for xx in range(x-1, -1, -1):
                        if rocks[y][xx] == '.':
                            spaces += 1
                        else:
                            break
    
                    xx = x - spaces
                    rocks[y][xx] = 'O'
                    rocks[y][x] = '.'

        return rocks

    def tilt_south(self, rocks):
        
        X = len(rocks[0])
        Y = len(rocks)

        for y in range(Y-1, -1, -1):
            for x in range(X):
                if rocks[y][x] == 'O':
        
                    # start looking at the row below for space to move
                    if y == Y-1: continue

                    # if there's no space to move, move to the next rock
                    if rocks[y+1][x] != '.': continue

                    # now travel down on the rock's column till we hit another rock or the 
                    # side of the map
                    spaces = 0
                    for yy in range(y+1, Y):
                        if rocks[yy][x] == '.':
                            spaces += 1
                        else:
                            break
    
                    yy = y + spaces
                    rocks[yy][x] = 'O'
                    rocks[y][x] = '.'

        return rocks

    def tilt_east(self, rocks):
        
        X = len(rocks[0])
        Y = len(rocks)

        for y in range(Y):
            for x in range(X-1, -1, -1):
                if rocks[y][x] == 'O':
        
                    # start looking at the column to the right for space to move
                    if x == X-1: continue

                    # if there's no space to move, move to the next rock
                    if rocks[y][x+1] != '.': continue

                    # now travel right on the rock's row till we hit another rock or the 
                    # side of the map
                    spaces = 0
                    for xx in range(x+1, X):
                        if rocks[y][xx] == '.':
                            spaces += 1
                        else:
                            break
    
                    xx = x + spaces
                    rocks[y][xx] = 'O'
                    rocks[y][x] = '.'

        return rocks

    def load_from_rock(self, ix, row, rocks):
        weight = len(rocks) - ix
        nrocks = sum([ rock == 'O' for rock in row ])
        return weight * nrocks 

    def load_on_north_pillars(self, rocks):
        return sum([ self.load_from_rock(ix, row, rocks) for ix, row in enumerate(rocks) ])
            
    def A(self):
       
        rocks = self.tilt_north(self.get_input())
        answer = self.load_on_north_pillars(rocks)

        if self.cmdline.testing:
            expected = 136
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer

    def cycle(self, rocks):

#       log.info('original input')
#       log.info('-'*10)
#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')

        rocks = self.tilt_north(rocks)
#       log.info('tilted north')
#       log.info('-'*10)
#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')

        rocks = self.tilt_west(rocks)
#       log.info('tilted west')
#       log.info('-'*10)
#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')

        rocks = self.tilt_south(rocks)
#       log.info('tilted south')
#       log.info('-'*10)
#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')

        rocks = self.tilt_east(rocks)
#       log.info('tilted east')
#       log.info('-'*10)
#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')

        return rocks, self.load_on_north_pillars(rocks)

    def find_pattern(self, sequence):

        period = 0
        nmatches = 0
        for p in range(int(len(sequence)/3), 1, -1):
            span = p * 2
            matches = sum([ sequence[i:i+p] == sequence[i+p:i+(2*p)] for i in range(len(sequence) - span) ])
#           log.info(f'p: {p}: matches: {matches}')
            if matches > nmatches:
                period = p
                nmatches = matches 

        # find the first occurence of the pattern
        base = 0
        for i in range(len(sequence)-period):
            if sequence[i:i+period] == sequence[i+period:i+(2*period)]:
                base = i
                break

        return base, period

    def B(self):
        
        rocks = self.get_input()
        sequence = []
        with open('sequence.txt', 'w') as f:
            for i in range(400):
                rocks, load = self.cycle(rocks)
                sequence.append(load)
                f.write(f'{load}\n')

        # find the repeating pattern in the output
        base, period = self.find_pattern(sequence)
        assert period > 0, f'could not find repeating pattern in sequence'
 
        pattern = sequence[base:base+period]
        log.info(f'period: {period}')
        log.info(f'base: {base}, pattern: {pattern}, len pattern: {len(pattern)}')

        ncycles = 1000000000
        offset = (ncycles-(base+1)) % period
        log.info(f'offset: {offset}')
        answer = pattern[offset]

        if self.cmdline.testing:
            expected = 64
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
