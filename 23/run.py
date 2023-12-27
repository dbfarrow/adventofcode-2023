#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict, deque

from shared.aoc import __AOC
from shared import log

#sys.setrecursionlimit(100000)


class Graph():

    def __init__(self, data, downhill_only=True):

        self.map = data
        self.downhill_only = downhill_only
        self.Y = len(data)
        self.X = len(data[0])

        self.adj = [ ['<',-1,0], ['^',0,-1], ['>',1,0], ['v',0,1] ]

        self.vertices = []
        self.edges = defaultdict(list)
        self.pathlens = []

        self.get_vertices()
        self.get_edges()

    def get_vertices(self):

        for y in range(self.Y):
            for x in range(self.X):
                # rocks can't be vertices
                if self.map[y][x] == '#': continue  

                # for each non-rock, count the number of non rocks around it
                nadj = 0
                for a in self.adj:
                    slope, dx, dy = a
                    if 0 <= (x+dx) < self.X and 0 <= (y+dy) < self.Y and self.map[y+dy][x+dx] != '#':
                        nadj += 1
                if nadj > 2:
                    self.vertices.append((x, y))

        # and add in the start and end
        self.vertices.append((1, 0))
        self.vertices.append((self.X-2, self.Y-1))

    def get_edges(self):

        for (vx, vy) in self.vertices:
            q = deque([(vx, vy, 0)])
            visited = set()

            while q:
                # grab the first node in the list
                x, y, d = q.popleft()
                
                # if we've seen it then move to the next
                if (x,y) in visited: continue

                # note that we've seen the node
                visited.add((x,y))

                # if we've arrived at a vertex (and it's not where we started), 
                # we've reached the end of the edge. Save it and move to the next
                # item in the queue
                if (x,y) in self.vertices and (x,y) != (vx,vy):
                    self.edges[(vx,vy)].append((x, y, d))
                    continue
                
                # otherwise, find it's neighbors and add them to the queue. each 
                # neighbor is one step further from the starting node
                for slope, dx, dy in self.adj:
                    if 0 <= x+dx < self.X and 0 <= y+dy < self.Y and self.map[y+dy][x+dx] != '#':
                        # we are on a non rock spot. if we can only go downhill, the make sure
                        # the any slope at this point is in the right direction
                        aslope = self.map[y+dy][x+dx]
                        if self.downhill_only and aslope in '<^>v' and aslope != slope: continue

                        # if we get here then we have another step along an edge. add it to the queue
                        q.append((x+dx, y+dy, d+1))
        
    def dsf(self):
        self.dsf_helper((1,0), 0, [(1,0)]) 
        log.info(f'there are {len(self.pathlens)} paths through the map')
        return self.pathlens

    def dsf_helper(self, start, distance, visited):

#       log.info(f'dsf_helper() - start: {start}, distance: {distance}, visited: {visited}')
        for ex, ey, ed in self.edges[start]:
#           log.info(f'dsf_helper(): checking edge ({ex}, {ey})')
            if (ex, ey) in visited: 
#               log.info(f'already visited ({ex},{ey})')
                continue
            if ey == self.Y-1: 
#               log.info(f'reached end at ({ex},{ey}): d = {distance+ed}')
                self.pathlens.append(distance + ed)
                return 
            else:
#               log.info(f'recursing from ({start}) to ({ex},{ey}), d={distance}, ed={ed}')
                visited.append((ex, ey))
                self.dsf_helper((ex, ey), distance + ed, visited)    
                visited.pop()
    
class AOC(__AOC):

    def __init__(self):
        super().__init__(day=23)

    def A(self):
       
        graph = Graph(self.get_input(), True)
#       log.info(f'num vertices: {len(graph.vertices)}')
#       [ log.info(v) for v in graph.vertices ]
#       log.info(f'num edges   : {len(graph.edges)}')
#       [ log.info(f'{k}: {v}') for k, v in graph.edges.items() ]
 
        all_paths = graph.dsf()
        answer = max(all_paths)
        if self.cmdline.testing:
            expected = 94
            assert answer == expected, f'Expected {expected}, got {answer}'

            also_expected = [ 74, 82, 82, 86, 90, 94 ]
            assert sorted(all_paths) == also_expected, f'Also expected {also_expected}, got {all_paths}'

        return answer


    def B(self):
        
        graph = Graph(self.get_input(), False)
#       log.info(f'num vertices: {len(graph.vertices)}')
#       [ log.info(v) for v in graph.vertices ]
#       log.info(f'num edges   : {len(graph.edges)}')
#       [ log.info(f'{k}: {v}') for k, v in graph.edges.items() ]

        all_paths = graph.dsf()
        answer = max(all_paths)

        if self.cmdline.testing:
            expected = 154
            assert answer == expected, f'Expected {expected}, got {answer}'
        return answer


if __name__ == "__main__":
    AOC().run()
