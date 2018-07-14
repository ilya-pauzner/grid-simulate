from queue import PriorityQueue
from functools import total_ordering
from time import sleep
from turtle import Turtle, Screen
from math import atan2, pi
from tkinter import *
from collections import Counter
import matplotlib.pyplot as plt


class Vector:
    def __init__(self, coords=(0, 0)):
        self.dimension = len(coords)
        self.coords = coords
        self.time = 0
        for elem in coords:
            self.time += elem * elem
        self.time = self.time ** 0.5 / 100


def calc(n):
    sqrt_n = n ** 0.5
    return sqrt_n / (int(sqrt_n))


SquareVectors = (Vector(coords=(100, 0)),
                 Vector(coords=(-100, 0)),
                 Vector(coords=(0, 100)),
                 Vector(coords=(0, -100)))

RectVectors = (Vector(coords=(100 * calc(17), 0)),
               Vector(coords=(-100 * calc(17), 0)),
               Vector(coords=(0, 100 * calc(19))),
               Vector(coords=(0, -100 * calc(19))))

HexVectors = (Vector(coords=(100, 0)),
              Vector(coords=(-50, 86.66)),
              Vector(coords=(-50, -86.66)),
              Vector(coords=(-100, 0)),
              Vector(coords=(50, 86.66)),
              Vector(coords=(50, -86.66))
              )

CubeVectors = (Vector(coords=(100, 0, 0)),
               Vector(coords=(-100, 0, 0)),
               Vector(coords=(0, 100, 0)),
               Vector(coords=(0, -100, 0)),
               Vector(coords=(0, 0, 100)),
               Vector(coords=(0, 0, -100)))

PVectors = (Vector(coords=(100 * calc(13), 0, 0)),
            Vector(coords=(-100 * calc(13), 0, 0)),
            Vector(coords=(0, 100 * calc(17), 0)),
            Vector(coords=(0, -100 * calc(17), 0)),
            Vector(coords=(0, 0, 100 * calc(19))),
            Vector(coords=(0, 0, -100 * calc(19))))

VECTORS = SquareVectors
DIMENSION = 2
DEPTH = 0
X = False
Y = False
Z = False


def goodx(v):
    return not (len(v) > 0 and X and v[0] < 0)


def goody(v):
    return not (len(v) > 1 and Y and v[1] < 0)


def goodz(v):
    return not (len(v) > 2 and Z and v[2] < 0)


def good(v):
    return goodx(v) and goody(v) and goodz(v)


@total_ordering
class GridPoint:
    def __init__(self, coords=(0, 0), vectors=None):
        self.coords = coords
        if vectors == None:
            vectors = VECTORS
        self.vectors = vectors
        self.dimension = len(coords)
        self.visible = (self.dimension == 2)

    def adj(self, now=0):
        res = []
        for v in self.vectors:
            tmp = tuple([self.coords[i] + v.coords[i] for i in range(self.dimension)])
            if good(tmp):
                res.append(GridPointEvent(round(now + v.time, 3), GridPoint(coords=tmp, vectors=self.vectors)))
        return res

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
    def __init__(self, time=1, point=None, turtle_coords=(0, 0), visible=None):
        self.time = time
        if point is None:
            point = GridPoint()
        if visible is None:
            visible = (DIMENSION == 2)
        self.point = point
        self.visible = visible
        if visible:
            self.turtle = Turtle()
            self.turtle.up()
            self.turtle.hideturtle()
            self.turtle.speed(0)
            self.turtle.setposition(*turtle_coords)
        else:
            self.turtle = None

    def __eq__(self, other):
        return (self.time, self.point) == (other.time, other.point)

    def __lt__(self, other):
        return (self.time, self.point) < (other.time, other.point)

    def __str__(self):
        return (self.time, self.point).__str__()


def anime():
    global DIMENSION
    DIMENSION = 2


def real_world():
    global DIMENSION
    DIMENSION = 3


def all():
    global X, Y, Z
    X = False
    Y = False
    Z = False


def semi():
    global X, Y, Z
    X = True
    Y = False
    Z = False


def quarter():
    global X, Y, Z
    X = True
    Y = True
    Z = False


def eight():
    global X, Y, Z
    X = True
    Y = True
    Z = True


def set_square():
    global VECTORS
    VECTORS = SquareVectors


def set_hex():
    global VECTORS
    VECTORS = HexVectors


def set_rect():
    global VECTORS
    VECTORS = RectVectors


def set_cube():
    global VECTORS
    VECTORS = CubeVectors


def set_par():
    global VECTORS
    VECTORS = PVectors


def choose_grid():
    global num
    for elem in window.grid_slaves():
        elem.destroy()
    if DIMENSION == 2:
        type = IntVar()
        square = Radiobutton(window, text="Квадратная", value=1, variable=type, command=set_square)
        square.grid(column=0, row=0)
        hex = Radiobutton(window, text="Шестиугольная", value=2, variable=type, command=set_hex, state=NORMAL)
        hex.grid(column=1, row=0)
        rect = Radiobutton(window, text="Прямоугольная", value=3, variable=type, command=set_rect, state=NORMAL)
        rect.grid(column=2, row=0)
    else:
        type = IntVar()
        cube = Radiobutton(window, text="Кубическая", value=1, variable=type, command=set_cube)
        cube.grid(column=0, row=0)
        par = Radiobutton(window, text="Параллелипипед", value=2, variable=type, command=set_par, state=NORMAL)
        par.grid(column=1, row=0)
    num = Entry(window, text='Глубина Симуляции')
    num.grid(column=0, row=1)
    start = Button(window, text='Старт', command=start_simulation)
    start.grid(column=0, row=2)


def start_simulation():
    global window
    window.quit()
    global DEPTH
    DEPTH = int(num.get())
    q = PriorityQueue()

    screen = Screen()
    text = Turtle()
    text.hideturtle()
    text.up()
    text.goto(-screen.screensize()[0], -screen.screensize()[1])
    text.write('0', font=("Arial", 16, "normal"))

    on_fire = set()
    NOW = 0
    start = GridPointEvent()
    answer = []
    if start.visible:
        start.turtle.showturtle()
    q.put(start)
    while not q.empty() and NOW <= DEPTH:
        cur = q.get()
        text.clear()
        text.write(str(NOW), font=("Arial", 16, "normal"))
        if NOW != cur.time:
            if NOW == DEPTH:
                break
            # new tic
            on_fire.clear()
            NOW = cur.time
        if cur.visible:
            cur.turtle.goto(*(cur.point.coords))
        if cur.point not in on_fire:
            for w in cur.point.adj(now=NOW):
                q.put(w)
                answer.append((0, cur.time))
                answer.append((1, w.time - 1e-9))
                if w.visible:
                    w.turtle.goto(*(cur.point.coords))
                    w.turtle.color('green')
                    w.turtle.shape('arrow')
                    w.turtle.setheading(
                        180 * atan2(w.point.coords[1] - cur.point.coords[1],
                                    w.point.coords[0] - cur.point.coords[0]) / pi)
                    w.turtle.down()
                    w.turtle.goto(w.point.coords[0] / 4 + 3 * cur.point.coords[0] / 4,
                                  w.point.coords[1] / 4 + 3 * cur.point.coords[1] / 4)
                    w.turtle.showturtle()
            on_fire.add(cur.point)
        if cur.visible:
            cur.turtle.color("red")
            cur.turtle.shape("circle")
    answer.sort()
    line = Counter()
    bal = 0
    for elem in answer:
        if elem[0] == 0:
            bal += 1
            line[elem[1]] = bal
        else:
            bal -= 1
    DATA = [(0, 0)]
    for elem in line:
        DATA.append((elem, line[elem]))
    DATA.sort()
    X = [DATA[0][0]]
    Y = [DATA[0][1]]
    for i in range(1, len(DATA)):
        X.append(DATA[i][0] - 1e-3)
        Y.append(DATA[i - 1][1])

        X.append(DATA[i][0])
        Y.append(DATA[i][1])
    plt.plot(X, Y)
    plt.show()
    screen.exitonclick()


window = Tk()
window.geometry('400x400')

dim = IntVar()
space = Radiobutton(window, text="3D", value=3, variable=dim, command=real_world, state=NORMAL)
space.grid(column=1, row=0)
plain = Radiobutton(window, text="2D", value=2, variable=dim, command=anime, state=NORMAL)
plain.grid(column=0, row=0)

border = IntVar()
half = Radiobutton(window, text="Половина", value=1, variable=border, command=semi, state=NORMAL)
half.grid(column=1, row=1)
quadrant = Radiobutton(window, text="Четверть", value=2, variable=border, command=quarter, state=NORMAL)
quadrant.grid(column=2, row=1)
octant = Radiobutton(window, text="Октант", value=3, variable=border, command=eight, state=NORMAL)
octant.grid(column=3, row=1)
whole = Radiobutton(window, text="Вся решетка", value=4, variable=border, command=all, state=NORMAL)
whole.grid(column=0, row=1)

start = Button(window, text='Старт', command=choose_grid)
start.grid(column=0, row=2)
window.mainloop()
