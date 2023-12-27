#!/usr/bin/env python3
import sys
sys.path.append('..')

from enum import Enum

from shared.aoc import __AOC
from shared import log

class Dir(Enum):
    LEFT=1
    RIGHT=2
    UP=3
    DOWN=4

class beam():

    __beamid = 0
    __maxx = __maxy = 0

    @staticmethod
    def set_maxes(x, y):
        beam.__maxx = x
        beam.__maxy = y    

    def __init__(self, l, d):

        beam.__beamid += 1
        self.beamid = beam.__beamid

        self.loc = l
        self.dir = d

    def __repr__(self):
        return f'beam[{self.beamid}]: {self.loc} {self.dir}'

    def __key(self):
        return (self.loc, self.dir)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, beam):
            return self.__key() == other.__key()
        return NotImplemented

    def next(self, tile):

        n = []

        if tile == '.':
            if self.dir == Dir.LEFT: n.append(self.left())
            elif self.dir == Dir.RIGHT: n.append(self.right())
            elif self.dir == Dir.UP: n.append(self.up())
            elif self.dir == Dir.DOWN: n.append(self.down())

        elif tile in '/':
            if self.dir == Dir.LEFT: n.append(self.down())
            elif self.dir == Dir.RIGHT: n.append(self.up())
            elif self.dir == Dir.UP: n.append(self.right())
            elif self.dir == Dir.DOWN: n.append(self.left())

        elif tile in '\\':
            if self.dir == Dir.LEFT: n.append(self.up())
            elif self.dir == Dir.RIGHT: n.append(self.down())
            elif self.dir == Dir.UP: n.append(self.left())
            elif self.dir == Dir.DOWN: n.append(self.right())

        elif tile in '|':
            if self.dir == Dir.LEFT or self.dir == Dir.RIGHT: 
                n.append(self.up())
                n.append(self.down())
            elif self.dir == Dir.UP: n.append(self.up())
            elif self.dir == Dir.DOWN: n.append(self.down())

        elif tile in '-':
            if self.dir == Dir.LEFT: n.append(self.left())
            elif self.dir == Dir.RIGHT: n.append(self.right())
            elif self.dir == Dir.UP or self.dir == Dir.DOWN:
                n.append(self.left())
                n.append(self.right())

        return n

    def left(self):
        return beam((self.loc[0]-1, self.loc[1]), Dir.LEFT) if self.loc[0] > 0 else None                # move left

    def right(self):
        return beam((self.loc[0]+1, self.loc[1]), Dir.RIGHT) if self.loc[0] < beam.__maxx-1 else None    # move right

    def up(self):
        return beam((self.loc[0], self.loc[1]-1), Dir.UP) if self.loc[1] > 0 else None                # move up
    
    def down(self):
        return beam((self.loc[0], self.loc[1]+1), Dir.DOWN) if self.loc[1] < beam.__maxy-1 else None    # move down

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=16)

    def do_the_thing(self, mapp, startbeam):

        mapp = self.get_input()
        beam.set_maxes(len(mapp[0]), len(mapp))

        beams = [ startbeam ]
        visited = set()
        ix = 0
        while len(beams) > 0:

#           log.info(f'loop[{ix}]: ---')
#           log.info(f'processing beams:')
#           [ log.info(b) for b in beams ]
#           log.info('')
 
            nextbeams = []

            for b in beams:

                # track the location we've visited
                visited.add(b)

                # what tile is at the current location? and where
                # do we need to go next. we may need to split
                tile = mapp[b.loc[1]][b.loc[0]]
                ns = b.next(tile)
#               log.info(f'{b}: tile: {tile}; ns: {ns}')
#               log.info('')

                nextbeams.extend([ n for n in ns if n and n not in visited ])

            beams = nextbeams
#           log.info(f'number of beams at end of loop: {len(beams)}')
#           log.info(f'--- end of loop[{ix}]')
#           log.info('')
            ix += 1
 

#       log.info('---')
#       log.info('visited:')
#       [ log.info(v) for v in visited ]
#       log.info(f'loop terminated at ix={ix} with len(beams) = {len(beams)}')

        return len(list(set([v.loc for v in visited ]))) 

    def A(self):
       

        mapp = self.get_input()
        beam.set_maxes(len(mapp[0]), len(mapp))
        answer = self.do_the_thing(mapp, beam((0,0), Dir.RIGHT))

        if self.cmdline.testing:
            expected = 46
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        answer = 0

        mapp = self.get_input()

        # from the top
        for i in range(len(mapp[0])):
            answer = max(answer, self.do_the_thing(mapp, beam((i, 0), Dir.DOWN)))
        
        # from the bottom
        for i in range(len(mapp[0])):
            answer = max(answer, self.do_the_thing(mapp, beam((i, len(mapp)-1), Dir.UP)))

        # from the left
        for i in range(len(mapp)):
            answer = max(answer, self.do_the_thing(mapp, beam((0, i), Dir.RIGHT)))

        for i in range(len(mapp[0])):
            answer = max(answer, self.do_the_thing(mapp, beam((len(mapp[0])-1, i), Dir.LEFT)))

        if self.cmdline.testing:
            expected = 51
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
