from django.contrib import admin
from .models import FriendRequest, Message

# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(Message)
