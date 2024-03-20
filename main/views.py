from django.shortcuts import render, redirect
from .forms import CreateUserForm, CustomAuthenticationForm, CampaignCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('name: '+username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # Return an 'invalid login' error message.
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')

            # Відправка привітання на електронну пошту
            subject = 'Welcome to Our Site!'
            message = f"Hello {request.user.username},\n\nWelcome to our site!"
            from_email = settings.EMAIL_HOST_USER
            to_email = email
            send_mail(subject, message, from_email, [to_email])

            return redirect('/')  # Перенаправити користувача на домашню сторінку після реєстрації
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile(request):
    user_campaigns = Campaign.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_campaigns': user_campaigns})


def create_campaign(request):
    if request.method == 'POST':
        form = CampaignCreationForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('success_page/')
    else:
        form = CampaignCreationForm()
    return render(request, 'campaign.html', {'form': form})


def success_page(request):
    return render(request, 'success_page.html')


def campaign_detail(request, campaign_name):
    campaign = Campaign.objects.get(campaign_name=campaign_name)

    return render(request, 'campaign_detail.html', {'campaign': campaign})


def donate(request):
    subject = 'Congratulations!'
    html_message = render_to_string('milestones.html', {'username': 'username'})  # ADD params
    from_email = settings.EMAIL_HOST_USER
    to_email = None  # edit
    send_mail(subject, html_message, from_email, [to_email])
