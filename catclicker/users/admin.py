from django.contrib import admin


from users.models import User, UserUpgrade

from game.models import Score


class ScoreInline(admin.TabularInline):
    model = Score

class UserUpgradeInline(admin.TabularInline):
    model = UserUpgrade
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 20
    list_filter = ['name']
    inlines = [ScoreInline, UserUpgradeInline]

@admin.register(UserUpgrade)
class UpdateAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ['user__name', 'upgrade']
    search_fields = ['user__name', "upgrade"]
# Register your models here.
