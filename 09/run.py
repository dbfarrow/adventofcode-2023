#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=9) # <----- fill in day here

    def get_input(self):

        readings = []
        for l in super().get_input():
            readings.append([ int(i) for i in l.split(' ') ])
        return readings
        
    def predict_next(self, series):

        nextss = [ series ]
        currs = series
        while not all([ currs[i] == 0 for i in range(len(currs)) ]):
            nexts = [ (currs[i+1] - currs[i]) for i in range(len(currs)-1)] 
            nextss.append(nexts)
            currs = nexts

#       for s in nextss:
#           log.info(f'{len(s)}: {s}')
#       log.info(' ')
 
        nextv = 0
        for i in range(len(nextss)-1, -1, -1):
            nextv += nextss[i][-1]
            nextss[i].append(nextv)
#           log.info(f'{len(nextss[i])}: {nextss[i]}')

#       log.info('---')
#       log.info(' ')
        return nextss[0]

    def A(self):
       
        answer = sum([ self.predict_next(i)[-1] for i in self.get_input() ])
        if self.cmdline.testing:
            expected = 114
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def predict_prev(self, series):

        nextss = [ series ]
        currs = series
        while not all([ currs[i] == 0 for i in range(len(currs)) ]):
            nexts = [ (currs[i+1] - currs[i]) for i in range(len(currs)-1)] 
            nextss.append(nexts)
            currs = nexts

#       for s in nextss:
#           log.info(f'{len(s)}: {s}')
#       log.info(' ')
 
        prevv = 0
        for i in range(len(nextss)-1, -1, -1):
            nextss[i].insert(0, nextss[i][0] - prevv)
            prevv = nextss[i][0]
#           log.info(f'{len(nextss[i])}: {nextss[i]}')

#       log.info('---')
#       log.info(' ')
        return nextss[0]

    def B(self):
        
        answer = [ self.predict_prev(i)[0] for i in self.get_input() ]
        log.info(answer)
        answer = sum(answer)
        if self.cmdline.testing:
            expected = 2
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
