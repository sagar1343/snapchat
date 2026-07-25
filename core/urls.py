from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register-user"),
    path("logout/", views.logout_view, name="logout"),
    path("search/", views.search_view, name="search-users"),
    path("send-invite/<int:id>", views.send_invite, name="send-invite"),
    path("chat-details/<int:id>", views.chat_details_view, name="chat-details"),
    path("send-message/<int:id>", views.send_message, name="send-message"),
]
