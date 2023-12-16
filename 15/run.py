#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
import re

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=15)

    def hash(self, s):
        h = 0
        for c in s:
            h += ord(c)
            h *= 17
            h %= 256
        return h

    def A(self):
       
        steps = self.get_input()[0].split(',')

        answer = 0
        for s in steps:
            h = self.hash(s)
#           log.info(f'{s} = {h}')
            answer += h

        if self.cmdline.testing:
            expected = 1320
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        steps = self.get_input()[0].split(',')
        boxes = defaultdict(list)

        for s in steps:
            match = re.match('([a-z]+)([=-])([1-9]?)', s)
            assert match, f'regex does not match {s}'
            (label, op, fl) = match.groups()
            fl = int(fl) if fl != '' else 0
            h = self.hash(label)
#           log.info(f'{s}: label: {label}, hash: {h}, op:{op}, fl: {fl}')

            if op == '-':
                boxes[h] = [ l for l in boxes[h] if l[0] != label ]
            elif op == '=':
                offset = [ ix for ix, lense in enumerate(boxes[h]) if lense[0] == label ]
                assert len(offset) <= 1, f'lense in box too many times: {boxes[h]}'
                if len(offset) == 1:
                    offset = sum(offset)
                    boxes[h][offset] = (label, fl)
                else:
                    boxes[h].append((label, fl))
 
            else:
                raise Exception(f'unknown operation: {op} in {s}')

        answer = 0
        for ix, b in boxes.items():
            for iy, s in enumerate(b):
                power = (ix + 1) * (iy + 1) * s[1]
                log.info(f'box {ix}: slot: {iy}: {s}, power: {power}')
                answer += power

        if self.cmdline.testing:
            expected = 145
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
