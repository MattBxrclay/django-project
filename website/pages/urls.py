from django.urls import path
from .views import HomePageView, AboutPageView, UserCreate, confirm_email, edit_profile
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('user/create/', UserCreate, name='UserCreate'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('confirm-email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('accounts/profile/', edit_profile, name='edit_profile'),
]
