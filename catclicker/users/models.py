from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    hashed_password = models.CharField(max_length=255)
    points_per_second = models.IntegerField(default=0)
    points_per_click = models.IntegerField(default=1)

    upgrades = models.ManyToManyField(
        'game.Upgrade',
        through='UserUpgrade',
        related_name='users'
    )


    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"

    def __str__(self):
        return self.name
    
# Pro uživatele automaticky vytvoříme záznam v databázi s jeho skóre.
@receiver(post_save, sender=User)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        from game.models import Score
        Score.objects.get_or_create(user=instance)

# Model pro ukládání všech uživatelských nákupů
class UserUpgrade(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_upgrades')
    upgrade = models.ForeignKey("game.Upgrade", on_delete=models.CASCADE, related_name='user_upgrades')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'upgrade')
        verbose_name = 'Vylepšení'
        verbose_name_plural = 'Vylepšení'

    def __str__(self):
        return f"Upgrade of {self.user.name}: {self.upgrade.name}"
