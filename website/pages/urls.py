# pages/urls.py
from django.urls import path
from .views import HomePageView, AboutPageView, UserCreate

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('user/create/', UserCreate, name='UserCreate'), # URL path for form
]