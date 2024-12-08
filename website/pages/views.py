# pages/views.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from pages.models import User
from pages.forms import UserForm

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

def UserCreate(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('UserCreate')
    else:
        form = UserForm()
    return render(request, 'user_create.html', {'form': form})
    
def home(request):
    form = UserForm(request.POST)
    user = User.objects.get(pk=1)
    return render(request, 'user_create.html', {'form': form})