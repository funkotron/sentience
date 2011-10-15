from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=20)
    exchange = models.CharField(max_length=20)

class Article(models.Model):
    name = models.CharField(max_length=255)
    entity = models.ForeignKey(Entity)
    src = models.CharField(max_length=255)
    date = models.DateField()
    body = models.TextField()

class Stock(models.Model):
    date = models.DateField()
    price = models.IntegerField()
    entity = models.ForeignKey(Entity)

