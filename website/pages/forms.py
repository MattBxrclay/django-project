from django import forms
from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = User
        fields = ['id','name', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
