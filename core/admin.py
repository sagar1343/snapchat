from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import FriendRequest, Message, SnapUser

# Register your models here.


class MyUserAdmin(UserAdmin):
    model = SnapUser
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("avatar",)}),)


admin.site.register(SnapUser, MyUserAdmin)
admin.site.register(FriendRequest)
admin.site.register(Message)
