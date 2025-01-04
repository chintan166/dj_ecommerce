from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name','address','contact']

class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']