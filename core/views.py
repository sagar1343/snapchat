from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from .utils import are_friends
from .models import FriendRequest, Message
from . import forms


# Create your views here.
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = forms.RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = forms.LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    friend_requests = FriendRequest.objects.filter(
        status=FriendRequest.StatusChoice.ACCEPTED
    ).filter(Q(from_user=request.user) | Q(to_user=request.user))

    friends = []
    for friend in friend_requests:
        if request.user == friend.from_user:
            friends.append(friend.to_user)
        else:
            friends.append(friend.from_user)
    return render(request, "pages/chat.html", {"friends": friends})


@login_required
def chat_details_view(request, id):
    friend = get_object_or_404(get_user_model(), pk=id)
    if not are_friends(request.user, friend):
        return redirect("home")

    messages = Message.objects.filter(
        Q(sender=request.user, reciever=friend)
        | Q(sender=friend, reciever=request.user)
    ).order_by("created_at")

    messages = list(messages)
    recieved_messages = Message.objects.filter(reciever=request.user, sender=friend)
    recieved_messages.delete()

    return render(
        request,
        "pages/chat-details.html",
        {"friend": friend, "chat_messages": messages},
    )


@login_required
def search_view(request):
    users = []
    friends = []
    unique_friends = []
    pending = []

    search_username = request.GET.get("username")
    if search_username:
        users = (
            get_user_model()
            .objects.filter(username__icontains=search_username)
            .exclude(id=request.user.id)
        )

        queryset = FriendRequest.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user)
        )

        friends = queryset.filter(status=FriendRequest.StatusChoice.ACCEPTED)
        pending_requests = queryset.filter(status=FriendRequest.StatusChoice.PENDING)

        for friend in friends:
            if request.user == friend.from_user:
                unique_friends.append(friend.to_user.id)
            else:
                unique_friends.append(friend.from_user.id)

        for req in pending_requests:
            if request.user == req.from_user:
                pending.append(req.to_user.id)
            else:
                pending.append(req.from_user.id)

    return render(
        request,
        "pages/search.html",
        {
            "users": users,
            "friends": unique_friends,
            "pending": pending,
            "search": search_username,
        },
    )


@require_http_methods(["POST"])
@login_required
def send_invite(request, id):
    if id == request.user.id:
        return redirect("search-users")
    to_user = get_object_or_404(get_user_model(), id=id)

    try:
        FriendRequest.objects.create(from_uxser=request.user, to_user=to_user)
    except IntegrityError:
        redirect("search-users")

    return redirect("search-users")


@login_required
@require_http_methods(["POST"])
def send_message(request, id):
    friend = get_object_or_404(get_user_model(), pk=id)

    if not are_friends(request.user, friend):
        return redirect("home")

    message = request.POST.get("message")
    snap = request.FILES.get("image")

    if message or snap:
        Message.objects.create(
            sender=request.user, reciever=friend, text=message, image=snap
        )
    return redirect("chat-details", id=id)


@login_required
@require_http_methods(["GET"])
def friend_request_list_view(request):
    friend_requests = FriendRequest.objects.filter(
        status=FriendRequest.StatusChoice.PENDING, to_user=request.user
    )
    return render(
        request, "pages/friend-request.html", {"friend_requests": friend_requests}
    )


@login_required
@require_http_methods(["POST"])
def accept_friend_request(request, id):
    req = get_object_or_404(FriendRequest, pk=id)
    if req.to_user == request.user and req.status == FriendRequest.StatusChoice.PENDING:
        req.status = FriendRequest.StatusChoice.ACCEPTED
        req.save()
    return redirect("friend-requests")
