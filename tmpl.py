#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=-1) # <----- fill in day here

    def A(self):
       
        answer = 0
        if self.cmdline.testing:
            expected = -1
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
