#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=4) 

    def get_input(self):
        
        winners = []
        numbers = []
        for l in super().get_input():
            (ws, ns) = l.split('|')

            (title, ws) = ws.split(':')
            winners.append([ int(w) for w in ws.split(' ') if w.isnumeric() ]) 
            numbers.append([ int(n) for n in ns.split(' ') if n.isnumeric() ]) 

        return winners, numbers

    def A(self):

        (winners, numbers) = self.get_input()
        answer = 0
        
        x = [ len(set(winners[i]).intersection(numbers[i])) for i in range(len(winners)) ]
        x = [ 2 ** (xx - 1) for xx in x if xx > 0 ]
        answer = sum(x)
        if self.cmdline.testing:
            assert answer == 13, f'Expected 13, got {answer}'
        return answer

    def B(self):

        (winners, numbers) = self.get_input()
        answer = 0
        
        cards = defaultdict(int)
        matches = [ len(set(winners[i]).intersection(numbers[i])) for i in range(len(winners)) ]
        
        for i in range(len(winners)):
            cards[i] += 1
            for j in range(matches[i]):
                cards[i+j+1] += cards[i]

        answer = sum(cards.values())
        if self.cmdline.testing:
            assert answer == 30, f'Expected 30, got {answer}'
        return answer

if __name__ == "__main__":
    AOC().run()
