from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, PlayerProfile, OrganizerProfile

@receiver(post_save, sender=User)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.PLAYER:
            PlayerProfile.objects.create(user=instance)
        elif instance.role == User.Role.ORGANIZER:
            OrganizerProfile.objects.create(user=instance)
