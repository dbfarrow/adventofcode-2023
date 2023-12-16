#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=14)

    def get_input(self):
        return [ list(l) for l in super().get_input() ]

    
    def tilt(self, rocks):
        
        for y in range(1, len(rocks)):
            for x in range(len(rocks[0])):
                if rocks[y][x] == 'O':

                    # start looking at the row above for space to move
                    yy = y - 1

                    # if there's no space to move, move to the next rock
                    if rocks[y-1][x] != '.': 
#                       log.info(f'({x}, {y}) cannot move')
                        continue

                    # now travel up the column above the rock till we hit another
                    # rock or the top of the map
                    spaces = 0
                    for yy in range(y - 1, -1, -1):
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

    def A(self):
       
        rocks = self.get_input()

#       [ log.info(''.join(r)) for r in rocks ]
#       log.info(' ')
        rocks = self.tilt(rocks)
#       log.info(' ')
#       [ log.info(''.join(r)) for r in rocks ]

        answer = 0
        for ix, row in enumerate(rocks):
            weight = len(rocks) - ix
            nrocks = sum([ rock == 'O' for rock in row ])
            answer += nrocks * weight

        if self.cmdline.testing:
            expected = 136
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        answer = 0
        if self.cmdline.testing:
            expected = -1
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
