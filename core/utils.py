from .models import FriendRequest, Chat
from django.db.models import Q


def are_friends(user1, user2):
    return (
        FriendRequest.objects.filter(
            Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1)
        )
        .filter(status=FriendRequest.StatusChoice.ACCEPTED)
        .exists()
    )


def get_friends(user):
    friend_requests = FriendRequest.objects.filter(
        status=FriendRequest.StatusChoice.ACCEPTED
    ).filter(Q(from_user=user) | Q(to_user=user))

    friends = []
    for fr in friend_requests:
        if user == fr.from_user:
            friends.append(fr.to_user)
        else:
            friends.append(fr.from_user)
    return friends


def get_or_create_chat(user1, user2):
    if user1.id > user2.id:
        user1, user2 = user2, user1
    chat, _ = Chat.objects.get_or_create(user1=user1, user2=user2)
    return chat
