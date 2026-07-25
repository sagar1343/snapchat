from django.contrib import admin
from .models import FriendRequest, Message, SnapUser

# Register your models here.
admin.site.register(SnapUser)
admin.site.register(FriendRequest)
admin.site.register(Message)
