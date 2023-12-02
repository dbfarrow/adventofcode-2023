#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from functools import reduce
import json

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=2) # <----- fill in day here

    def get_input(self):
        
        data = super().get_input()
        games = {}
        for l in data:
            game, draws = l.split(':')
            g, n = game.split(' ')
            v = []

            draws = draws.split(';')
            dd = []
            for draw in draws:
                cubes = draw.split(',')
                d = {}
                for color in cubes:
                    count, c = color.strip().split(' ')
                    d[c] = int(count)
                dd.append(d)

            v.append(dd)
            games[int(n)] = v
                
#       log.info(json.dumps(games, indent=2))
        return games

    def ispossible(self, game, spec):

        for draws in game:
            for draw in draws:
                if any([ True for k, v in draw.items() if v > spec[k] ]):
                    return False

        return True

    def A(self):

        spec = { 'red': 12, 'green': 13, 'blue': 14 }

        games = self.get_input()
        possible = [ game for game, draws in games.items() if self.ispossible(draws, spec) ]
        answer = sum(possible)

        if self.cmdline.testing:
            assert answer == 8, f'expected 8, got {answer}'

        return answer

    def B(self):

        games = self.get_input()

        powers = []
        for game, draws in games.items():
            colors = defaultdict(int)
            for draw in draws:
                for cubes in draw:
                    for color, count in cubes.items():
                        colors[color] = max(count, colors[color]) 
                powers.append(reduce((lambda x, y: x * y), [ v for v in colors.values () ]))

        answer = sum(powers)
        if self.cmdline.testing:
            assert answer == 2286, f'expected 2286, got {answer}'

        return answer

if __name__ == "__main__":
    AOC().run()
