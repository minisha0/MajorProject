from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



# USER MODEL WITH ROLES
class User(AbstractUser):
    class Role(models.TextChoices):
        PLAYER = "PLAYER", "Player"
        JUDGE = "JUDGE", "Judge"
        ORGANIZER = "ORGANIZER", "Organizer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PLAYER,
    )

    def is_player(self):
        return self.role == self.Role.PLAYER

    def is_judge(self):
        return self.role == self.Role.JUDGE

    def is_organizer(self):
        return self.role == self.Role.ORGANIZER


# PLAYER 
class PlayerProfile(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player_profile")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    body_weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    weight_class = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to="player_profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# ORGANIZER 
class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organizer_profile")
    organization_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="organizer_profiles/", blank=True, null=True)
    total_events_created = models.PositiveIntegerField(default=0)
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.organization_name})"
