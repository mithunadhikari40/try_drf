from django.db import models

"""This is just a abstract class so that it records all the timestamps on when the record was created and updated,
   Since it is already extending Model class, classes which extend it do not need to extend Model
   We don't want any migrations for it, so turning it off on Meta class"""


class TimeStamp(models.Model):
    # auto_now_add adds an entry for first time only
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now adds an entry every time it is updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
