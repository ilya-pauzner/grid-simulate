from queue import PriorityQueue
from functools import total_ordering
from turtle import Turtle, Screen
from math import atan2, pi
from tkinter import Button, Entry, Radiobutton, Tk, IntVar, StringVar
from collections import Counter
import matplotlib.pyplot as plt

COLORS = ['green', 'blue', 'black']


class Vector:
    def __init__(self, coords=(0, 0), time=None):
        self.dimension = len(coords)
        self.coords = coords
        self.time = time
        if time is None:
            self.time = 0
            for elem in coords:
                self.time += elem * elem
            self.time = self.time ** 0.5 / 100


def calc(n):
    sqrt_n = n ** 0.5
    return sqrt_n / (int(sqrt_n))


PossibleVectors = {'SquareVectors': (Vector(coords=(100, 0), time=1),
                                     Vector(coords=(-100, 0), time=1),
                                     Vector(coords=(0, 100), time=1),
                                     Vector(coords=(0, -100), time=1)),

                   'RectVectors': (Vector(coords=(100 * calc(17), 0)),
                                   Vector(coords=(-100 * calc(17), 0)),
                                   Vector(coords=(0, 100 * calc(19))),
                                   Vector(coords=(0, -100 * calc(19)))),

                   'HexVectors': (Vector(coords=(100, 0), time=1),
                                  Vector(coords=(-50, 86.66), time=1),
                                  Vector(coords=(-50, -86.66), time=1),
                                  Vector(coords=(-100, 0), time=1),
                                  Vector(coords=(50, 86.66), time=1),
                                  Vector(coords=(50, -86.66), time=1)
                                  ),

                   'CubeVectors': (Vector(coords=(100, 0, 0), time=1),
                                   Vector(coords=(-100, 0, 0), time=1),
                                   Vector(coords=(0, 100, 0), time=1),
                                   Vector(coords=(0, -100, 0), time=1),
                                   Vector(coords=(0, 0, 100), time=1),
                                   Vector(coords=(0, 0, -100), time=1)),

                   'PVectors': (Vector(coords=(100 * calc(13), 0, 0)),
                                Vector(coords=(-100 * calc(13), 0, 0)),
                                Vector(coords=(0, 100 * calc(17), 0)),
                                Vector(coords=(0, -100 * calc(17), 0)),
                                Vector(coords=(0, 0, 100 * calc(19))),
                                Vector(coords=(0, 0, -100 * calc(19)))),

                   'DiamondVectors': (Vector(coords=(100, 100, 100), time=1),
                                      Vector(coords=(-100, 100, 100), time=1),
                                      Vector(coords=(100, -100, 100), time=1),
                                      Vector(coords=(-100, -100, 100), time=1),
                                      Vector(coords=(100, 100, -100), time=1),
                                      Vector(coords=(-100, 100, -100), time=1),
                                      Vector(coords=(100, -100, -100), time=1),
                                      Vector(coords=(-100, -100, -100), time=1))
                   }

VECTORS = PossibleVectors['SquareVectors']
DIMENSION = 2
DEPTH = 0
X = False
Y = False
Z = False
time_texts = {'1.0308': 'sqrt(17) / int(sqrt(17))', '1.0897': 'sqrt(19) / int(sqrt(19))'}


def make_name():
    ans = ''
    if Z:
        ans = 'octant of '
    elif Y:
        ans = 'quarter of '
    elif X:
        ans = 'half of '
    if VECTORS == PossibleVectors['SquareVectors']:
        ans += 'square'
    if VECTORS == PossibleVectors['RectVectors']:
        ans += 'rectangle'
    if VECTORS == PossibleVectors['HexVectors']:
        ans += 'hexagonal'
    if VECTORS == PossibleVectors['CubeVectors']:
        ans += 'cubic'
    if VECTORS == PossibleVectors['PVectors']:
        ans += 'parallelipiped'
    if VECTORS == PossibleVectors['DiamondVectors']:
        ans += 'diamond'
    return ans


def goodx(v):
    return not (len(v) > 0 and X and v[0] < 0)


def goody(v):
    return not (len(v) > 1 and Y and v[1] < 0)


def goodz(v):
    return not (len(v) > 2 and Z and v[2] < 0)


def good(v):
    return goodx(v) and goody(v) and goodz(v)


def complicated_good(w):
    if VECTORS == PossibleVectors['DiamondVectors']:
        v = (w[0] // 100, w[1] // 100, w[2] // 100)
        return (v[0] % 2 == v[1] % 2 == v[2] % 2) and (sum(v) % 4 in (0, 1))
    return True


@total_ordering
class GridPoint:
    def __init__(self, coords=None, vectors=None):
        if vectors is None:
            vectors = VECTORS
        self.vectors = vectors
        self.dimension = vectors[0].dimension
        if coords is None:
            coords = tuple([0] * self.dimension)
        self.coords = coords
        self.visible = (self.dimension == 2)
        print(coords)

    def adj(self, now=0):
        res = []
        for v in self.vectors:
            tmp = tuple([self.coords[i] + v.coords[i] for i in range(self.dimension)])
            if good(tmp) and complicated_good(tmp):
                res.append(GridPointEvent(round(now + v.time, 4), GridPoint(coords=tmp, vectors=self.vectors)))
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


def set_grid_type():
    global VECTORS, PossibleVectors, grid_type
    VECTORS = PossibleVectors[grid_type.get()]


def choose_grid():
    global num, grid_type
    grid_type = StringVar()
    for elem in window.grid_slaves():
        elem.destroy()
    if DIMENSION == 2:
        square = Radiobutton(window, text="Квадратная", value='SquareVectors', variable=grid_type,
                             command=set_grid_type)
        square.grid(column=0, row=0)
        hex = Radiobutton(window, text="Шестиугольная", value='HexVectors', variable=grid_type, command=set_grid_type)
        hex.grid(column=1, row=0)
        rect = Radiobutton(window, text="Прямоугольная", value='RectVectors', variable=grid_type, command=set_grid_type)
        rect.grid(column=2, row=0)
    else:
        cube = Radiobutton(window, text="Кубическая", value='CubeVectors', variable=grid_type, command=set_grid_type)
        cube.grid(column=0, row=0)
        par = Radiobutton(window, text="Параллелипипед", value='PVectors', variable=grid_type, command=set_grid_type)
        par.grid(column=1, row=0)
        diam = Radiobutton(window, text="Алмаз", value='DiamondVectors', variable=grid_type, command=set_grid_type)
        diam.grid(column=2, row=0)
    num = Entry(window, text='Глубина Симуляции')
    num.grid(column=0, row=1)
    start = Button(window, text='Старт', command=start_simulation)
    start.grid(column=0, row=2)


def start_simulation():
    global window
    window.quit()
    global DEPTH
    s = num.get()
    if s == '':
        s = '4'
    DEPTH = int(s)
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
        times = [round(v.time, 4) for v in VECTORS]
        times.sort()
        times = list(set(times))
        colors = dict()
        for i in range(len(times)):
            colors[times[i]] = COLORS[i]

        time_turtles = [Turtle() for t in times]
        for i in range(len(time_turtles)):
            time_turtles[i].hideturtle()
            time_turtles[i].up()
            time_turtles[i].goto(screen.screensize()[0] - 100, screen.screensize()[1] - i * 50)
            time_turtles[i].down()
            time_turtles[i].width(3)
            time_turtles[i].color(colors[times[i]])
            time_turtles[i].forward(50)
            time_text = str(times[i])
            if time_text in time_texts:
                time_text = time_texts[time_text]
            time_turtles[i].write(time_text)

        start.turtle.showturtle()
    q.put(start)
    while not q.empty() and NOW <= DEPTH:
        cur = q.get()

        print(cur.point)

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
                answer.append((cur.time, 0))
                answer.append((w.time - 1e-9, 1))
                if w.visible:
                    w.turtle.goto(*(cur.point.coords))
                    # w.turtle.color('green')

                    dt = w.time - cur.time
                    time_index = 0
                    for i in range(len(times)):
                        if abs(dt - times[i]) < abs(dt - times[time_index]):
                            time_index = i
                    w.turtle.color(colors[times[time_index]])
                    w.turtle.width(3)

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
    print(answer)
    line = Counter()
    bal = 0
    for elem in answer:
        if elem[1] == 0:
            bal += 1
            line[elem[0]] = bal
        else:
            bal -= 1
    DATA = [(0, 0)]
    for elem in line:
        DATA.append((elem, line[elem]))
    DATA.sort()
    X = [DATA[0][0]]
    Y = [DATA[0][1]]
    for i in range(1, len(DATA)):
        X.append(DATA[i][0] - 1e-6)
        Y.append(DATA[i - 1][1])

        X.append(DATA[i][0])
        Y.append(DATA[i][1])
    for i in range(len(X)):
        print(X[i], Y[i])
    plt.plot(X, Y)
    plt.title('N(t) graph in ' + make_name() + ' grid')
    plt.xlabel('Time')
    plt.ylabel('Quantity of particles')
    plt.show()
    screen.exitonclick()


window = Tk()
window.geometry('400x400')

dim = IntVar()
space = Radiobutton(window, text="3D", value=3, variable=dim, command=real_world, )
space.grid(column=1, row=0)
plain = Radiobutton(window, text="2D", value=2, variable=dim, command=anime, )
plain.grid(column=0, row=0)

border = IntVar()
half = Radiobutton(window, text="Половина", value=1, variable=border, command=semi, )
half.grid(column=1, row=1)
quadrant = Radiobutton(window, text="Четверть", value=2, variable=border, command=quarter, )
quadrant.grid(column=2, row=1)
octant = Radiobutton(window, text="Октант", value=3, variable=border, command=eight, )
octant.grid(column=3, row=1)
whole = Radiobutton(window, text="Вся решетка", value=4, variable=border, command=all, )
whole.grid(column=0, row=1)

start = Button(window, text='Старт', command=choose_grid)
start.grid(column=0, row=2)
window.mainloop()
