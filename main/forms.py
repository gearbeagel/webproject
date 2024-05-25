from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Campaign


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=15, label='',
                               widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Логін'}))
    password = forms.CharField(max_length=20, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=15, label='',
                               widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Створіть логін'}))
    password1 = forms.CharField(max_length=20, label='',
                               widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Створіть пароль'}))
    password2 = forms.CharField(max_length=20, label='',
                                widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Повторіть пароль'}))
    email = forms.EmailField(max_length=20, label='',
                             widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'E-mail'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class CampaignCreationForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['campaign_name', 'description', 'campaign_logo', 'goal']


class CampaignDonateForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['donate']
