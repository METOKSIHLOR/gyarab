from django.contrib import admin


from users.models import User, UserUpgrade

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(UserUpgrade)
class UpdateAdmin(admin.ModelAdmin):
    search_fields = ['user__name', "upgrade_name"]
# Register your models here.
