from django.contrib import admin

from game.models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    search_fields = ['user__name']
    list_filter = ['user']
    list_per_page = 20
# Register your models here.
