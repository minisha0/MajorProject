from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import PlayerProfile, OrganizerProfile

@login_required
def profile_view(request):
    user = request.user

    if user.is_player():
        profile = user.player_profile
        return render(request, "users/player_profile.html", {"profile": profile})

    elif user.is_organizer():
        profile = user.organizer_profile
        return render(request, "users/organizer_profile.html", {"profile": profile})

    return render(request, "users/profile_not_found.html")

