from django.contrib import admin


from users.models import User, UserUpgrade

admin.site.register(User)
admin.site.register(UserUpgrade)
# Register your models here.
