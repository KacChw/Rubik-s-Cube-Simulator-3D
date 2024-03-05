from vpython import *
import numpy as np
import random
from rozwiazanie import *


class Kostka():

    def __init__(self):
        self.counter = 0
        self.running = True
        self.tiles = []
        self.dA = np.pi / 40
        self.moves_history = []  # dodana lista do przechowywania historii ruchów
        # center

        wspol_scianek = [[vector(-1, 1, 1.5), vector(0, 1, 1.5), vector(1, 1, 1.5),  # front
                     vector(-1, 0, 1.5), vector(0, 0, 1.5), vector(1, 0, 1.5),
                     vector(-1, -1, 1.5), vector(0, -1, 1.5), vector(1, -1, 1.5), ],
                    [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),  # right
                     vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
                     vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
                    [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),  # back
                     vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
                     vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),  # left
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),  # top
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
                    [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),  # bottom
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
                    ]
        colors = [vector(1, 0, 0), vector(1, 1, 0), vector(1, 0.5, 0), vector(1, 1, 1), vector(0, 0, 1),
                  vector(0, 1, 0)]
        angle = [(0, vector(0, 0, 0)), (np.pi / 2, vector(0, 1, 0)), (0, vector(0, 0, 0)),
                 (np.pi / 2, vector(0, 1, 0)), (np.pi / 2, vector(1, 0, 0)), (np.pi / 2, vector(1, 0, 0))]
        # sides
        for rank, side in enumerate(wspol_scianek):
            for vec in side:
                tile = box(pos=vec, size=vector(0.98, 0.98, 0.1), color=colors[rank])
                tile.rotate(angle=angle[rank][0], axis=angle[rank][1])
                self.tiles.append(tile)
        # positions
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        # variables
        self.rotate = [None, 0, 0]
        self.moves = []

    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4:
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['top'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['bottom'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])

    def animations(self):
        if self.rotate[0] == 'front_counter':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_counter':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_counter':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_counter':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_counter':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_counter':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'front_clock':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=-self.dA, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_clock':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=-self.dA, axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_clock':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_clock':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=-self.dA, axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_clock':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=-self.dA, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_clock':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=-self.dA, axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        if self.rotate[1] + self.dA / 2 > self.rotate[2] > self.rotate[1] - self.dA / 2:
            self.rotate = [None, 0, 0]
            self.reset_positions()

    def rotate_front_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("F'")
            self.rotate = ['front_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_right_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("R'")
            self.rotate = ['right_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_back_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("B'")
            self.rotate = ['back_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_left_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("L'")
            self.rotate = ['left_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_top_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("U'")
            self.rotate = ['top_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_bottom_counter(self):
        if self.rotate[0] is None:
            self.moves_history.append("D'")
            self.rotate = ['bottom_counter', 0, np.pi / 2]
            self.counter = 1

    def rotate_front_clock(self):
        self.moves_history.append("F")
        if self.rotate[0] is None:
            self.rotate = ['front_clock', 0, np.pi / 2]
            self.counter = 1

    def rotate_right_clock(self):
        if self.rotate[0] is None:
            self.moves_history.append("R")
            self.rotate = ['right_clock', 0, np.pi / 2]
            self.counter = 1

    def rotate_back_clock(self):
        self.moves_history.append("B")
        if self.rotate[0] is None:
            self.rotate = ['back_clock', 0, np.pi / 2]
            self.counter = 1

    def rotate_left_clock(self):
        self.moves_history.append("L")
        if self.rotate[0] is None:
            self.rotate = ['left_clock', 0, np.pi / 2]
            self.counter = 1

    def rotate_top_clock(self):
        self.moves_history.append("U")
        if self.rotate[0] is None:
            self.rotate = ['top_clock', 0, np.pi / 2]
            self.counter = 1

    def rotate_bottom_clock(self):
        self.moves_history.append("D")
        if self.rotate[0] is None:
            self.rotate = ['bottom_clock', 0, np.pi / 2]
            self.counter = 1

    def undo_move(self):

        if len(self.moves_history) > 0:
            last_move = self.moves_history.pop()

            if last_move == "F":
                self.rotate_front_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "R":
                self.rotate_right_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "B":
                self.rotate_back_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "L":
                self.rotate_left_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "U":
                self.rotate_top_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "D":
                self.rotate_bottom_counter()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "F'":
                self.rotate_front_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "R'":
                self.rotate_right_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "B'":
                self.rotate_back_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "L'":
                self.rotate_left_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "U'":
                self.rotate_top_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()
            elif last_move == "D'":
                self.rotate_bottom_clock()
                if len(self.moves_history) > 1:
                    self.moves_history.pop()

    def move(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        if self.rotate[0] is None and len(self.moves) > 0:
            if self.moves[0] == possible_moves[0]:
                self.moves_history.append(self.moves[0])
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[1]:
                self.moves_history.append(self.moves[0])
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[2]:
                self.moves_history.append(self.moves[0])
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[3]:
                self.moves_history.append(self.moves[0])
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[4]:
                self.moves_history.append(self.moves[0])
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[5]:
                self.moves_history.append(self.moves[0])
                self.rotate_bottom_clock()
            elif self.moves[0] == possible_moves[6]:
                self.moves_history.append(self.moves[0])
                self.rotate_front_counter()
            elif self.moves[0] == possible_moves[7]:
                self.moves_history.append(self.moves[0])
                self.rotate_right_counter()
            elif self.moves[0] == possible_moves[8]:
                self.moves_history.append(self.moves[0])
                self.rotate_back_counter()
            elif self.moves[0] == possible_moves[9]:
                self.moves_history.append(self.moves[0])
                self.rotate_left_counter()
            elif self.moves[0] == possible_moves[10]:
                self.moves_history.append(self.moves[0])
                self.rotate_top_counter()
            elif self.moves[0] == possible_moves[11]:
                self.moves_history.append(self.moves[0])
                self.rotate_bottom_counter()
            self.moves.pop(0)

    def scramble(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        for i in range(25):
            self.moves.append(random.choice(possible_moves))

    def solution(self):
        solve(self.tiles)




    def solve(self):
        values = solve(self.tiles)
        values = list(values.split(" "))
        for value in values:
            lis_value = list(value)
            if lis_value[-1] == '2':
                lis_value.pop(-1)
                value = ''.join(lis_value)
                self.moves.append(value)
                self.moves.append(value)
            else:
                self.moves.append(value)

    def control(self):
        button(bind=self.rotate_front_clock, text='F')
        button(bind=self.rotate_front_counter, text="F'")
        button(bind=self.rotate_right_clock, text='R')
        button(bind=self.rotate_right_counter, text="R'")
        button(bind=self.rotate_back_clock, text='B')
        button(bind=self.rotate_back_counter, text="B'")
        button(bind=self.rotate_left_clock, text='L')
        button(bind=self.rotate_left_counter, text="L'")
        button(bind=self.rotate_top_clock, text='U')
        button(bind=self.rotate_top_counter, text="U'")
        button(bind=self.rotate_bottom_clock, text='D')
        button(bind=self.rotate_bottom_counter, text="D'")
        button(bind=self.scramble, text='random_move')
        button(bind=self.solution, text='solution')
        button(bind=self.solve, text='solve it!')
        button(bind=self.undo_move, text='undo')


    def update(self):
        rate(60)
        self.animations()
        self.move()

    def start(self):
        self.reset_positions()
        self.control()
        while self.running:
            self.update()


cube = Kostka()
cube.start()

