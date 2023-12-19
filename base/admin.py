from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined',)



@admin.register(FriendRequest)
class FRAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at',)