import datetime

from django.contrib.auth.models import User
from django.db import models


class Matrix(models.Model):
    columns = models.IntegerField(blank=False)
    rows = models.IntegerField(blank=False)
    mines = models.IntegerField(blank=False)


class Box(models.Model):
    # Assuming 99 as representation of mines to do it simpler
    MINE = 99

    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=True)
    has_flag = models.BooleanField(default=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def sum(self):
        self.value += 1
        self.save()

    def press(self):
        self.is_hidden = False
        self.save()

    def set_flag(self):
        self.has_flag = True
        self.save()

    def put_mine(self):
        self.value = self.MINE
        self.save()


class Game(models.Model):
    INITIAL = 'I'
    STARTED = 'S'
    WON = 'W'
    LOST = 'L'
    STATUS_CHOICES = [
        (INITIAL, 'Initial'),
        (STARTED, 'Started'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INITIAL)
    started_time = models.DateTimeField()
    ended_time = models.DateTimeField()
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)

    def get_status(self):
        return self.get_status_display()

    def get_played_time(self):
        if self.status != self.STARTED:
            raise RuntimeError('Game not started yet')
        return self.started_time - self.ended_time

    def start_game(self):
        self.status = self.STARTED
        self.started_time = datetime.datetime.now()
        self.save()

    def lose_game(self):
        self.status = self.LOST
        self.ended_time = datetime.datetime.now()
        self.save()

    def win_game(self):
        self.status = Game.WON
        self.ended_time = datetime.datetime.now()
        self.save()

    def to_string(self):
        return {
            'user': self.user.username,
            'status': self.get_status_display(),
            'started_time': self.started_time.strftime('%m-%d-%Y %H:%M') if self.started_time else '-'
        }
