from django.db import models


class Link(models.Model):
    link = models.CharField(max_length=2048)

class MapWord(models.Model):
    word = models.CharField(max_length=140)
    frequency = models.IntegerField()

class Myword(models.Model):
    word = models.CharField(max_length=140)
    links = models.ManyToManyField(Link, blank=True, related_name="links")
    map_words = models.ManyToManyField(MapWord, blank=True, related_name="map_words")






