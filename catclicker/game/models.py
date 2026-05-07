from django.db import models
from django.utils import timezone
from datetime import timedelta

from users.models import User


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='score')
    points = models.BigIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def update_points(self):
        now = timezone.now()
        delta = now - self.last_updated
        seconds_passed = int(delta.total_seconds())

        if seconds_passed >= 1:
            self.points += seconds_passed * self.user.points_per_second
            self.last_updated += timedelta(seconds=seconds_passed)
            self.save(update_fields=['points', 'last_updated'])

        return self.points