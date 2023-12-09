#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from functools import cmp_to_key

from shared.aoc import __AOC
from shared import log

class hand:

    def __init__(self, l, jacks_wild):
        self.cards, self.bid = l.split(' ')
        self.parsed = defaultdict(int)
        self.jacks = sum([ 1 for c in self.cards if c == 'J' ])
        self.jacks_wild = jacks_wild
        for c in self.cards:
            self.parsed[c] += 1

        self.counts = defaultdict(int)
        for v in self.parsed.values():
            self.counts[v] += 1

        if jacks_wild:
            self.calc_rank_jacks_wild()
        else:
            self.calc_rank()

    def __repr__(self):
        cc = ' '.join([ str(self.counts[i]) for i in range(5, 0, -1) ])
        return f' [ { cc } ] rank={self.rank}.{self.jacks}: {self.cards} for {self.bid}     --{"j"*self.jacks}'
        
    def calc_rank(self):
        if (self.counts[5] == 1):
            self.rank = 7       # five of a kind
        elif (self.counts[4] == 1):
            self.rank = 6       # four of a kind
        elif (self.counts[3] == 1 and self.counts[2] == 1):
            self.rank = 5       # full house
        elif self.counts[3] == 1:
            self.rank = 4       # three of a kind
        elif self.counts[2] == 2:
            self.rank = 3       # two pairs
        elif self.counts[2] == 1:
            self.rank = 2       # one pair
        else:
            self.rank = 1       # high card


    def calc_rank_jacks_wild(self):

        self.counts[self.jacks] -= 1

        # -- five of a kind
        # five of a kind
        # four of a kind and a jack
        if (self.counts[5] == 1) \
            or (self.counts[4] == 1 and self.jacks == 1) \
            or (self.counts[3] == 1 and self.jacks == 2) \
            or (self.counts[2] == 1 and self.jacks == 3) \
            or (self.counts[1] == 1 and self.jacks == 4):
            self.rank = 7                                   

        # -- four of a kind
        # three of a kind and jack
        # a pair and a pair of jacks
        elif (self.counts[4] == 1) \
            or (self.counts[3] == 1 and self.jacks == 1) \
            or (self.counts[2] == 1 and self.jacks == 2) \
            or (self.counts[1] == 2 and self.jacks == 3):
            self.rank = 6                                   

        # -- full house
        # three of kind and a pair
        # two pairs and a jack
        elif (self.counts[3] == 1 and self.counts[2] == 1) \
            or (self.counts[2] == 2 and self.jacks == 1):   
            self.rank = 5                                   

        # -- three of a kind
        # three of a kind
        # a pair and jack
        # highcard and a pair of jacks
        elif self.counts[3] == 1 \
            or (self.counts[2] == 1 and self.jacks == 1) \
            or (self.counts[1] == 3 and self.jacks == 2):\
            self.rank = 4                                   

        # -- two pairs
        # two pair
        # a pair and a jack
        elif (self.counts[2] == 2) \
            or (self.counts[2] == 1 and self.jacks == 1):   
            self.rank = 3                                   

        # -- one pair
        # highcard and a jack
        elif (self.counts[2] == 1) \
            or (self.counts[1] >= 4 and self.jacks == 1):   
            self.rank = 2                                   
        
        # highcard
        else:
            self.rank = 1                                   


def compare(x, y):
    
    cards = {}
    if x.jacks_wild:
        cards = { 'J': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
                '7': 7, '8': 8, '9': 9, 'T': 10, 'Q': 12, 'K': 13, 'A': 14 }
    else:
        cards = { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 }

    diff = x.rank - y.rank
    if diff == 0:
        for j in range(len(x.cards)):
            if x.cards[j] != y.cards[j]:
                diff = cards[x.cards[j]] - cards[y.cards[j]]
                break
    return diff

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=7)

    def evaluate_hands(self, jacks_wild=False):

        hands = sorted([ hand(l, jacks_wild) for l in self.get_input() ], key=cmp_to_key(compare))
        for h in hands:
            log.info(h)

        return sum([ (ix + 1) * int(h.bid) for ix, h in enumerate(hands) ])

    def A(self):

        answer = self.evaluate_hands(jacks_wild=False)
        if self.cmdline.testing:
            expected = 6440
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        answer = self.evaluate_hands(jacks_wild=True)
        if self.cmdline.testing:
            expected = 5905
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
