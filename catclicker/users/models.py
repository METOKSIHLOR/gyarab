from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    hashed_password = models.CharField(max_length=255)
    points_per_second = models.IntegerField(default=0)
    points_per_click = models.IntegerField(default=1)

@receiver(post_save, sender=User)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        from game.models import Score
        Score.objects.get_or_create(user=instance)
