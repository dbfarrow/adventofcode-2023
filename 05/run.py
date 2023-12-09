#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=5)

    def get_input(self):
        
        seeds = []
        maps = defaultdict(list)
        key = None

        for l in super().get_input():

            if l.startswith('seeds:'):
                (_, s) = l.split(':')
                seeds = [ int(i) for i in s.strip().split(' ') ]
            elif l == "":
                key = None
            elif ':' in l:
                key = l
            else:
                if key:
                    maps[key].append ([ int(i) for i in l.split(' ') ])
            
        return seeds, maps

    def src2dest(self, src, mapp):

        for (mdest, msrc, mrange) in mapp:
            if src >= msrc and src <  (msrc + mrange):
                dest = mdest + (src - msrc)
                return dest

        return src

    def A(self):

        seeds, maps = self.get_input()
        log.info(seeds)
        maps = maps.values()
            
        locs = {}
        for seed in seeds:
            src = seed
            for m in maps:
                dest = self.src2dest(src, m)
#               log.info(f'src: {src} -> dest: {dest}')
                src = dest 
            locs[seed] = dest
#           log.info(' ') 
#       log.info(locs)
        answer = min(locs.values())

        if self.cmdline.testing:
            assert answer == 35, f'Expected 35, got {answer}'
        return answer

    def B(self):

        ranges, maps = self.get_input()
        seeds = []
        total = 0
        for i in range(0, len(ranges), 2):
            total += ranges[i+1]
#           for j in range(ranges[i+1]):
#               seeds.append(ranges[i]+j)

        maps = maps.values()
            
        log.info(f'there are {total} seeds')
        return

        locs = {}
        for seed in seeds:
            src = seed
            for m in maps:
                dest = self.src2dest(src, m)
#               log.info(f'src: {src} -> dest: {dest}')
                src = dest 
            locs[seed] = dest
#           log.info(' ') 
#       log.info(locs)
        answer = min(locs.values())

        if self.cmdline.testing:
            assert answer == 46, f'Expected 46, got {answer}'
        return answer

if __name__ == "__main__":
    AOC().run()
