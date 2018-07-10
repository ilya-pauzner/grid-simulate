from queue import PriorityQueue
from functools import total_ordering
from time import perf_counter, sleep
from sys import argv
from turtle import Turtle, Screen
from math import atan2, pi


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
    def __init__(self, time=1, point=GridPoint(), turtle_coords=(0, 0)):
        self.time = time
        self.point = point
        self.turtle = Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.speed(SPEED)
        self.turtle.setposition(*turtle_coords)

    def __eq__(self, other):
        return (self.time, self.point) == (other.time, other.point)

    def __lt__(self, other):
        return (self.time, self.point) < (other.time, other.point)

    def __str__(self):
        return (self.time, self.point).__str__()


class SquareGridPoint(GridPoint):
    def __init__(self, coords=(0, 0)):
        super().__init__(coords=coords,
                         vectors=(Vector(coords=(100, 0)),
                                  Vector(coords=(-100, 0)),
                                  Vector(coords=(0, 100)),
                                  Vector(coords=(0, -100))))


class SquareGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=SquareGridPoint(), turtle_coords=(0, 0)):
        super().__init__(time, point, turtle_coords)


class HexGridPoint(GridPoint):
    def __init__(self, coords=(0, 0)):
        super().__init__(coords=coords,
                         vectors=(Vector(coords=(100, 0)),
                                  Vector(coords=(-50, 87)),
                                  Vector(coords=(-50, -87)),
                                  Vector(coords=(-100, 0)),
                                  Vector(coords=(50, 87)),
                                  Vector(coords=(50, -87))
                                  ))


class HexGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=HexGridPoint()):
        super().__init__(time, point)


class CubeGridPoint(GridPoint):
    def __init__(self, coords=(0, 0, 0)):
        super().__init__(dimension=3, coords=coords,
                         vectors=(Vector(dimension=3, coords=(1, 0, 0)),
                                  Vector(dimension=3, coords=(-1, 0, 0)),
                                  Vector(dimension=3, coords=(0, 1, 0)),
                                  Vector(dimension=3, coords=(0, -1, 0)),
                                  Vector(dimension=3, coords=(0, 0, 1)),
                                  Vector(dimension=3, coords=(0, 0, -1))))


class CubeGridPointEvent(GridPointEvent):
    def __init__(self, time=1, point=CubeGridPoint()):
        super().__init__(time, point)


print(argv)
q = PriorityQueue()
screen = Screen()
on_fire = set()
depth = int(argv[1])
NOW = 0
SPEED = 10
if argv[2] == 'S':
    start = SquareGridPointEvent()
if argv[2] == 'H':
    start = HexGridPointEvent()
if argv[2] == 'C':
    start = CubeGridPointEvent()
if len(argv) > 3 and argv[3] == 'slow':
    SPEED = 1
text = Turtle()
text.hideturtle()
text.up()
text.goto(-screen.screensize()[0], -screen.screensize()[1])
text.write('N(0) = 0', font=("Arial", 16, "normal"))
answer = [0] * depth
start.turtle.showturtle()
q.put(start)
while not q.empty() and NOW <= len(answer):
    cur = q.get()
    if NOW != cur.time:
        if NOW == len(answer):
            break
        # new tic
        text.clear()
        text.write('N(' + str(NOW + 1) + ') = ' + str(q.qsize() + 1), font=("Arial", 16, "normal"))
        answer[NOW] = q.qsize() + 1
        print(NOW, q.qsize(), perf_counter())
        on_fire.clear()
        NOW = cur.time
        sleep(5)
    cur.turtle.goto(*(cur.point.coords))
    # print(cur)
    if cur.point not in on_fire:
        for w in cur.point.adj(now=NOW):
            q.put(w)
            w.turtle.goto(*(cur.point.coords))
            w.turtle.color('green')
            w.turtle.shape('arrow')
            w.turtle.setheading(
                180 * atan2(w.point.coords[1] - cur.point.coords[1], w.point.coords[0] - cur.point.coords[0]) / pi)
            w.turtle.down()
            w.turtle.goto(w.point.coords[0] / 4 + 3 * cur.point.coords[0] / 4,
                          w.point.coords[1] / 4 + 3 * cur.point.coords[1] / 4)
            w.turtle.showturtle()
        on_fire.add(cur.point)
    cur.turtle.color("red")
    cur.turtle.shape("circle")
print(answer)
for i in range(1, len(answer)):
    print(answer[i] / (i * i))
screen.exitonclick()
