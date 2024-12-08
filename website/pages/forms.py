# pages/forms.py

from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']