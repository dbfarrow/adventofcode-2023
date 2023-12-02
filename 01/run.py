#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=1)

    def get_input(self):
        data = super().get_input()
        return [ d for d in data if d[0] != '#' ]

    def calculate_all(self, data):
        total = 0
        for d in data:
            ints = [ c for c in d if c.isnumeric() ]
            assert len(ints) >= 1, "need at least 1 ints in the string: {}".format(ints)
            dint = int("{}{}".format(ints[0], ints[-1]))
            log.info(f'{d} -> {dint}')
            total += dint
        return total

    def calculate(self, d):

#       log.info(d)
        ints = [ c for c in d if c.isnumeric() ]
        assert len(ints) >= 1, "need at least 1 ints in the string: {}".format(ints)
        di = int("{}{}".format(ints[0], ints[-1]))
#       log.info(f'{d} -> {di}')
        return di

    def replacewords(self, d):
        words = {
            "oneight": 18,
            "twone": 21,
            "threeight": 38,
            "fiveight": 58,
            "sevenine": 79,
            "eightwo": 82,
            "eighthree": 83,
            "nineight": 98,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
    
        D = d
        for i in range(len(d)):
            for k, v in words.items():
                dd = d[i:i+len(k)]
                if dd == k:
                    d = d.replace(k, str(v), 1)
#                   log.info(f"replaced {k} with {v}: d = {d}")
                    break

#       log.info(f"{D} -> {d}")
        return d

    def A(self):
        
        data = self.get_input()
        total = sum([ self.calculate(d) for d in data ])
        return total

    def B(self):
        data = self.get_input()
        total = 0
        for d in data:
            dr = self.replacewords(d)
            di = self.calculate(dr)
            log.info(f'{d} -> {dr} -> {di}')
            total += di

        return total

if __name__ == "__main__":
    AOC().run()
