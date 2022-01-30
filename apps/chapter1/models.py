from django.db import models

from apps.utils.timestamp.models import TimeStamp


class Student(TimeStamp):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
