from django.contrib.auth.models import User
from django.db import models


class Matrix(models.Model):
    columns = models.IntegerField(blank=False)
    rows = models.IntegerField(blank=False)
    mines = models.IntegerField(blank=False)


class Box(models.Model):
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=True)
    has_flag = models.BooleanField(default=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)

