from django.db import models

from users.models import User


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='score')
    points = models.BigIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


