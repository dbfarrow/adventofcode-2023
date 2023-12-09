#!/usr/bin/env python3
import sys
sys.path.append('..')

from functools import reduce
import re
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=6)

    def get_input(self, partb):

        for l in super().get_input():
            l = re.sub(' +', ' ' if not partb else '', l)
            if l.startswith('Time:'):
                (_, times) = l.split(':')
                times = list(map(int, times.strip().split(' ')))
            if l.startswith('Distance:'):
                (_, distances) = l.split(':')
                distances = list(map(int, distances.strip().split(' ')))

        return tuple(zip(times, distances))

    def calc_answer(self, data):

        all_beats = []
        for (time, distance) in data:
            mid = int(time / 2)
            beats = 0
            for i in range(mid, 0, -1):
                if (time - i) * i > distance:
                    beats += 1
                else:
                    break

            for i in range(mid + 1, time):
                if (time - i) * i > distance:
                    beats += 1
                else:
                    break

            all_beats.append(beats)
#           beats = [ ((time - i) * i) for i in range(time) if ((time - i) * i) > distance ]
#           log.info(beats)
#           all_beats.append(len(beats))
#           log.info(f'beats for ({time}, {distance}: {beats}')

        return reduce(lambda x, y: x * y, all_beats)

    def A(self):

        answer = 0

        data = self.get_input(False)
        log.info(data)

        answer = self.calc_answer(data)
        if self.cmdline.testing:
            expected = 288
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer

    def B(self):

        answer = 0

        data = self.get_input(True)
        log.info(data)

        answer = self.calc_answer(data)
        if self.cmdline.testing:
            expected = 71503
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer

if __name__ == "__main__":
    AOC().run()
