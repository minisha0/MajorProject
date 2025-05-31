from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, PlayerProfile, OrganizerProfile


# Customizing the User admin
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role",)


# PlayerProfile admin
@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "body_weight", "weight_class", "created_at")
    search_fields = ("user__username",)
    list_filter = ("gender", "weight_class")


# OrganizerProfile admin
@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization_name", "contact_number", "total_events_created", "notifications_enabled")
    search_fields = ("user__username", "organization_name")
