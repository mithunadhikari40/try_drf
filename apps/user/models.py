from django.db import models

from apps.utils.timestamp.models import TimeStamp

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

"""This method will be called as soon as there is some insertion in this model AUTH_USER_MODEL. We also can use 
similar action in our use case too """


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Student(TimeStamp):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
