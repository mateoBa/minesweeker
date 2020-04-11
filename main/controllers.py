from random import randrange
from main.models import *


class MatrixController:
    def __init__(self, columns, rows, mines):
        self.columns = columns
        self.rows = rows
        self.mines = mines
        self.matrix = Matrix.objects.create()

    def get_mines_in_matrix(self):
        mines = []
        while self.mines != len(mines):
            position = (randrange(self.columns), randrange(self.rows))
            if position not in mines:
                mines.append(position)

        return mines

    def _analyze_and_sum(self, query):
        if query:
            query.first().sum()

    def _calculate_adjacent_boxes(self, x, y):
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                if xn == x and yn == y:
                    continue
                box = Box.objects.filter(matrix=self.matrix, x=xn, y=yn)
                self._analyze_and_sum(box)

    def draw_matrix(self):
        mines = self.get_mines_in_matrix()
        for x in range(self.columns):
            for y in range(self.rows):
                box = Box.objects.create()
                box.x = x
                box.y = y
                box.matrix = self.matrix

                if (x, y) in mines:
                    box.value = Box.MINE
                    self._calculate_adjacent_boxes(x, y)

                box.save()


class GameController:
    pass
