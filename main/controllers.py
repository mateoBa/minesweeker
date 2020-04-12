from random import randrange
from main.models import *


class MatrixController:
    def __init__(self, matrix=None):
        self.matrix = matrix

    def create_matrix(self, columns, rows, mines):
        self.matrix = Matrix.objects.create(columns=columns, rows=rows, mines=mines)

    def get_mines_in_matrix(self):
        mines = []
        while self.matrix.mines != len(mines):
            position = (randrange(self.matrix.columns), randrange(self.matrix.rows))
            if position not in mines:
                mines.append(position)

        return mines

    def _adjacent_boxes(self, x, y, fun):
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                fun(xn, yn)

    def _sum_adjacent_boxes(self, x, y):
        box_query = Box.objects.filter(matrix=self.matrix, x=x, y=y)
        if box_query and box_query.first().value != Box.MINE:
            box_query.first().sum()

    def draw_matrix(self):
        mines = self.get_mines_in_matrix()
        print(f'mines in {mines}')
        for x in range(self.matrix.columns):
            for y in range(self.matrix.rows):
                box = Box.objects.create(x=x, y=y, matrix=self.matrix)
                if (x, y) in mines:
                    box.put_mine()

        for x, y in mines:
            self._adjacent_boxes(x, y, self._sum_adjacent_boxes)

    def get_matrix(self):
        self.draw_matrix()
        return self.matrix

    def _press(self, box):
        box.press()
        if box.value == Box.MINE:
            return False

        if box.value == 0:
            self._adjacent_boxes(box.x, box.y, self.check_and_press)
        return True

    def check_and_press(self, x, y):
        box = Box.objects.filter(matrix=self.matrix, x=x, y=y)
        if box and box.first().is_hidden:
            return self._press(box.first())

    def get_boxes(self, is_hidden):
        return Box.objects.filter(matrix=self.matrix, is_hidden=is_hidden)

    def check_win_case(self):
        return self.get_boxes(is_hidden=False).count() + self.matrix.mines == self.matrix.rows * self.matrix.columns


class GameController:
    def __init__(self, user, game=None, matrix_controller=None):
        self.user = user
        self.game = game
        self.matrix_controller = matrix_controller

    def create_game(self, columns, rows, mines):
        self.matrix_controller = MatrixController()
        self.matrix_controller.create_matrix(columns, rows, mines)
        self.game = Game.objects.create(user=self.user, matrix=self.matrix_controller.get_matrix())

    def press_box_and_check_status(self, x, y):
        if not self.matrix_controller.get_boxes(is_hidden=False):
            self.game.start_game()
            if not self.matrix_controller.check_and_press(x, y):
                self.game.lose_game()
        elif not self.matrix_controller.check_and_press(x, y):
            self.game.lose_game()
        elif self.matrix_controller.check_win_case():
            self.game.win_game()


class UserController:
    @classmethod
    def get_games_by_user(cls, user):
        games = Game.objects.filter(user=user)
        return [g.to_string() for g in games]

    @classmethod
    def create_game(cls, user, columns, rows, mines):
        # todo: check the correct number of columns, rows and mines
        game_controller = GameController(user)
        game_controller.create_game(int(columns), int(rows), int(mines))
        SettingUser.create_or_save(user, game_controller.game)
        return game_controller.matrix_controller.matrix.to_string()

    @classmethod
    def press(cls, user, game, x, y):
        matrix_controller = MatrixController(game.matrix)
        game_controller = GameController(user, game, matrix_controller)
        game_controller.press_box_and_check_status(x, y)
        return game_controller.game.to_string()
