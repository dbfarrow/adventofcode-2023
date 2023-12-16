#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=13)

    def get_input(self):
        
        lines = super().get_input()
        notes = []
        note = []
        for l in lines:
            if len(l) == 0:
                notes.append(note)
                note = []
            else:
                note.append(list(l))

        notes.append(note)
        return notes

    def find_vertical_reflection(self, note, logging=False):
            
        for i in range(1, len(note[0])):

            # slice the note into two sides at the requested column
            left = [ n[0:i] for n in note ]
            right = [ n[i:] for n in note ]

            # make the sides the same size
            if len(left[0]) < len(right[0]):
                right = [ r[0:len(left[0])] for r in right ]
            elif len(right[0]) < len(left[0]):
                left = [ l[-len(right[0]):] for l in left ]

            # reverse the right side
            right = [ r[::-1] for r in right ]

            # and compare them
            matches = [ left[i] == right[i] for i in range(len(left)) ]

            if logging:
                log.info(f'i = {i}')
                [ log.info(x) for x in left ]
                log.info(' ')
                [ log.info(x) for x in right ]
                log.info(f'{matches}')
                if all(matches): log.info(f'reflects horizontally at i={i}')
                log.info('---')

            if all(matches):
                return i


        return -1

    def find_horizontal_reflection(self, note, logging=False):

        for i in range(1, len(note)):

            # slice the note into two sides at the requested row
            bottom = note[0:i]
            top = note[i:]

            # make the sides the same size
            if len(top) < len(bottom):
                bottom = bottom[-len(top):]
            elif len(bottom) < len(top):
                top = top[0:len(bottom)]

            # reverse the bottom side
            bottom.reverse()

            if logging:
                log.info(f'i = {i}')
                [ log.info(x) for x in bottom ]
                log.info(' ')
                [ log.info(x) for x in top ]

            # and compare them
            matches = [ bottom[i] == top[i] for i in range(len(bottom)) ]

            if logging:
                log.info(f'i = {i}')
                [ log.info(x) for x in left ]
                log.info(' ')
                [ log.info(x) for x in right ]
                log.info(f'{matches}')
                if all(matches): log.info(f'reflects horizontally at i={i}')
                log.info('---')

            if all(matches):
                return i

        return -1


    def A(self):
       
        answer = 0
        notes = self.get_input()

        for n in notes:
            v = self.find_vertical_reflection(n)
            if v >= 0: answer += v
            h = self.find_horizontal_reflection(n)
            if h >= 0: answer += (h * 100)

        if self.cmdline.testing:
            expected = 405
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


    def B(self):
        
        logging = False
        answer = 0
        notes = self.get_input()
        
        for i, n in enumerate(notes):

#           if i != 7: continue

            hset = set()
            vset = set()

            log.info('----')
#           [log.info(nn) for nn in n ]
            # find the original reflection lines with the smudge since, apparently,
            # the msudge moves that original line. testing shows that fixing the 
            # smudge can craete reflections on both axes and we aren't supposed to 
            # count those
            h = self.find_horizontal_reflection(n, False)
            v = self.find_vertical_reflection(n, False)
            fixedh = fixedv = -1

            squares = [ (x, y) for y in range(len(n)) for x in range(len(n[0])) ]
            
            for (x, y) in squares:

                # try unsmudging this square
                unsmudged = n[y][x]
                n[y][x] = ('.' if unsmudged == '#' else '#')

                fixedh = self.find_horizontal_reflection(n, logging)
                fixedv = self.find_vertical_reflection(n, logging)
#               log.info(f'smudge at ({x},{y}) v: {v} -> {fixedv}; h: {h} -> {fixedh}')

                if fixedh > 0 and fixedh != h: hset.add(fixedh)
                if fixedv > 0 and fixedv != v: vset.add(fixedv)

                # unsmudge the square for the next round
                n[y][x] = unsmudged

#               if fixedh >= 0 and fixedh != h: 
#                   log.info(f'fixing smudge at ({x},{y}) v: {v} -> {fixedv}; h: {h} -> {fixedh}')
#               if fixedv >= 0 and fixedv != v: 
#                   log.info(f'fixing smudge at ({x},{y}) v: {v} -> {fixedv}; h: {h} -> {fixedh}')

            log.info(f'v: {v}, vset: {vset}')
            log.info(f'h: {h}, hset: {hset}')

            if len(vset) == 0 and len(hset) == 0: 
                log.info(f'expected a reflection line of some sort in note[{i}]: v={v}, h={h}')
                [ log.info(nn) for nn in n ]
                if v >= 0: vset.add(v)
                if h >= 0: hset.add(h)

            assert len(vset) <= 1, f'expected only one reflection line in vset: {vset}'
            assert len(hset) <= 1, f'expected only one reflection line in hset: {hset}'

            if len(vset) == 1: answer += list(vset)[0]
            if len(hset) == 1: answer += list(hset)[0] * 100

        if self.cmdline.testing:
            expected = 400
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
