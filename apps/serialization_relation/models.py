from django.db import models

from apps.utils.timestamp.models import TimeStamp


class Singer(TimeStamp):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Song(TimeStamp):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return self.title
