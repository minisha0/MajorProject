from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('registrations/', include('registrations.urls')),
    path('announcements/', include('announcements.urls')),
    path('livegame/', include('livegame.urls')),
]

