from django import forms
from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = User
        fields = ['id','name', 'email', 'password', 'role']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control w-50'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change your password.",
    )

    class Meta:
        model = User
        fields = ['name', 'email']  # Name and email fields