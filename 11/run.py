#!/usr/bin/env python3
import sys
sys.path.append('..')

import itertools 


from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=11)

    def calc_pathlen(self, p, empty_rows, empty_cols, expansion):
        
        (a, b) = p
    
        ex = sum([ 1 for c in empty_cols if c > min(a[0], b[0]) and c < max(a[0], b[0]) ])
        ey = sum([ 1 for r in empty_rows if r > min(a[1], b[1]) and r < max(a[1], b[1]) ])
        
        e = expansion - 1
        xdiff = abs(p[1][0] - p[0][0])
        ydiff = abs(p[1][1] - p[0][1])
        pathlen = xdiff + ydiff + (ex * e) + (ey * e)
        return pathlen


    def solve(self, expansion=2):
       
        mapp = self.get_input()
        empty_rows = [ ix for ix, row in enumerate(mapp) if '#' not in row ]
        empty_cols = []
        for x in range(len(mapp[0])):
            cvs = not any([ row[x] for row in mapp if row[x] == '#'])
            if cvs: empty_cols.append(x)

        # get all galaxies, calculate the distances between each pair, and sum up the distances
        g = [(x, y) for x in range(len(mapp[0])) for y in range(len(mapp)) if mapp[y][x] == '#' ]
        paths = itertools.combinations(g, 2)
        log.info(f'summing paths across {len(g)} galaxies')
        return sum([ self.calc_pathlen(x, empty_rows, empty_cols, expansion) for x in itertools.combinations(g, 2) ])

    def A(self):
       
        answer = self.solve(expansion=2)
        if self.cmdline.testing:
            expected = 374
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        answer = self.solve(expansion=1000000)
        if self.cmdline.testing:
            expected = 8410
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
