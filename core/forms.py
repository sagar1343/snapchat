from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "avatar"]


class LoginForm(AuthenticationForm):
    pass
