from django.urls import path
from users.views import profile_view
from . import views

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('resend-activation/', views.resend_activation_view, name='resend_activation'),
]
