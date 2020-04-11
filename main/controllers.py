import datetime

from random import randrange
from main.models import *


class MatrixController:
    def __init__(self, columns, rows, mines):
        self.matrix = Matrix.objects.create(columns=columns, rows=rows, mines=mines)
        self.matrix.save()

    def get_mines_in_matrix(self):
        mines = []
        while self.matrix.mines != len(mines):
            position = (randrange(self.matrix.columns), randrange(self.matrix.rows))
            if position not in mines:
                mines.append(position)

        return mines

    def _analyze_and_sum(self, box_query):
        if box_query:
            box_query.first().sum()

    def _calculate_adjacent_boxes(self, x, y):
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                if xn == x and yn == y:
                    continue
                self._analyze_and_sum(Box.objects.filter(matrix=self.matrix, x=xn, y=yn))

    def draw_matrix(self):
        mines = self.get_mines_in_matrix()
        for x in range(self.matrix.columns):
            for y in range(self.matrix.rows):
                box = Box.objects.create(x=x, y=y, matrix=self.matrix)

                if (x, y) in mines:
                    box.value = Box.MINE
                    self._calculate_adjacent_boxes(x, y)

                box.save()

    def get_matrix(self):
        self.draw_matrix()
        return self.matrix

    def press(self, x, y):
        pass


class GameController:
    def __init__(self, user, columns, rows, mines):
        self.matrix_controller = MatrixController(columns, rows, mines)
        self.game = Game.objects.create(user=user, matrix=self.matrix_controller.get_matrix())
        self.game.save()

    def start_game(self):
        self.game.status = Game.STARTED
        self.game.started_time = datetime.datetime.now()

    def check_status(self):
        if self.game.status == Game.INITIAL:
            self.start_game()
        else:
            # change to win or lost
            pass

    def press_box(self, x, y):
        self.matrix_controller.press(x, y)
        self.check_status()
