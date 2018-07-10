
from queue import PriorityQueue
from functools import total_ordering
from time import perf_counter
from sys import argv

class Vector:
    def __init__(self, dimension=2, coords=(0, 0), time=1):
        self.dimension = dimension
        self.coords = coords
        self.time = time


@total_ordering
class GridPoint:
    def __init__(self, dimension=2, coords=(0, 0), vectors=(Vector())):
        self.coords = coords
        self.vectors = vectors
        self.dimension = dimension

    def adj(self, now=0):
        return [GridPointEvent(now + v.time,
GridPoint(dimension=self.dimension, coords=tuple(
            [self.coords[i] + v.coords[i] for i in
range(self.dimension)]), vectors=self.vectors)) for v in
                self.vectors]

    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.coords < other.coords

    def __str__(self):
        return self.coords.__str__()

    def __hash__(self):
        return self.coords.__hash__()


@total_ordering
class GridPointEvent:
    def __init__(self, time=1, point=GridPoint()):
        self.time = time
        self.point = point

    def __eq__(self, other):
        return (self.time, self.point) == (other.time, other.point)

    def __lt__(self, other):
        return (self.time, self.point) < (other.time, other.point)

    def __str__(self):
        return (self.time, self.point).__str__()


class SquareGridPoint(GridPoint):
    def __init__(self, coords=(0, 0)):
        super().__init__(coords=coords,
                         vectors=(Vector(coords=(1, 0)),
                                  Vector(coords=(-1, 0)),
                                  Vector(coords=(0, 1)),
                                  Vector(coords=(0, -1))))


class SquareGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=SquareGridPoint()):
        super().__init__(time, point)


class HexGridPoint(GridPoint):
    def __init__(self, coords=(0, 0)):
        super().__init__(coords=coords,
                         vectors=(Vector(coords=(1, 0)),
                                  Vector(coords=(0, 1)),
                                  Vector(coords=(-1, -1))))


class HexGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=HexGridPoint()):
        super().__init__(time, point)


class CubeGridPoint(GridPoint):
    def __init__(self, coords=(0, 0, 0)):
        super().__init__(dimension=3, coords=coords,
                         vectors=(Vector(dimension=3, coords=(1, 0, 0)),
                         Vector(dimension=3, coords=(-1, 0,0)),
                                  Vector(dimension=3, coords=(0, 1, 0)),
                                  Vector(dimension=3, coords=(0, -1,0)),
                                  Vector(dimension=3, coords=(0, 0, 1)),
                                  Vector(dimension=3, coords=(0, 0,-1))))


class CubeGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=CubeGridPoint()):
        super().__init__(time, point)

print(argv)
q = PriorityQueue()

on_fire = set()
depth = int(argv[1])
NOW = 0
if argv[2] == 'S':
    start = SquareGridPointEvent()
if argv[2] == 'H':
    start = HexGridPointEvent()
if argv[2] == 'C':
    start = CubeGridPointEvent()
q.put(start)
answer = [0] * depth
while not q.empty() and NOW < len(answer):
    cur = q.get()
    if NOW != cur.time:
        # new tic
        answer[NOW] = q.qsize()
        print(NOW, q.qsize(), perf_counter())
        on_fire.clear()
        NOW = cur.time
    # print(cur)
    if cur.point not in on_fire:
        for w in cur.point.adj(now=NOW):
            q.put(w)
        on_fire.add(cur.point)
print(answer)
for i in range(1, len(answer)):
    print(answer[i] / (i * i))
