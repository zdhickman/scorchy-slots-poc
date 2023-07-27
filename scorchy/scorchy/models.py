from django.db import models

class Roll(models.Model):
    user_id = models.CharField(max_length=10)
    fruit_0 = models.CharField(max_length=10)
    fruit_1 = models.CharField(max_length=10)
    fruit_2 = models.CharField(max_length=10)
    fruit_3 = models.CharField(max_length=10)
    is_holdable = models.BooleanField()
    is_rollover = models.BooleanField()
    feature_sum = models.IntegerField()

class Holds(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    hold_0 = models.BooleanField()
    hold_1 = models.BooleanField()
    hold_2 = models.BooleanField()
    hold_3 = models.BooleanField()

class Jackpot(models.Model):
    jackpot = models.IntegerField()