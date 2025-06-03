from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from .tokens import token_generator
from .forms import RegisterForm
from .models import User, PlayerProfile, OrganizerProfile


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.activation_sent_at = now()
            user.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            html_message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(
                'Activate Your Account',
                'Click the link to activate your account.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message
            )

            messages.success(request, "Check your email to activate your account.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if user.activation_sent_at and now() > user.activation_sent_at + timedelta(minutes=10):
            return render(request, 'activation_expired.html', {'user': user})

        user.is_active = True
        user.email_verified = True  
        user.save()
        messages.success(request, "Your account has been activated. You can log in now.")
        return redirect('login')
    else:
        return render(request, 'activation_invalid.html')


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


def resend_activation_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                user.activation_sent_at = now()
                user.save()

                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

                html_message = render_to_string('activation_email.html', {
                    'user': user,
                    'activation_link': activation_link,
                })

                send_mail(
                    'Resend Activation Link',
                    'Click the link to activate your account.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message
                )
                messages.success(request, "Activation email resent.")
            else:
                messages.info(request, "Account is already active.")
        except User.DoesNotExist:
            messages.error(request, "No user with that email.")
        return redirect('resend_activation')

    return render(request, 'resend_activation.html')
