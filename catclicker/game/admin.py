from django.contrib import admin

from game.models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    search_fields = ['user__name']
# Register your models here.
