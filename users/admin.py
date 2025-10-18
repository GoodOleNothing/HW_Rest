from django.contrib import admin

from materials.models import Subscription
from users.models import User


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'city', 'is_active')


@admin.register(Subscription)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course')
