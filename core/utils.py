from .models import FriendRequest
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
