from django.shortcuts import render, redirect
from .forms import CreateUserForm, CustomAuthenticationForm, CampaignCreationForm, CampaignDonateForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign, Donors
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
    campaigns = Campaign.objects.all()
    return render(request, 'home.html', {'campaigns': campaigns})



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


def profile(request, user_name):
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
    if request.method == 'POST':
        form = CampaignDonateForm(request.POST)
        if form.is_valid():

            value = form.cleaned_data.get('donate')

            if Donors.objects.filter(user=request.user.username).exists() and Donors.objects.filter(campaign=campaign.campaign_name).exists():
                donor = Donors.objects.filter(user=request.user.username, campaign=campaign.campaign_name)
                donor = donor.first()
                donor.donate += value
                donor.save()
            else:
                donor = Donors.objects.create(user=request.user.username, campaign=campaign.campaign_name, donate=value)
                donor.save()

            if campaign.donate is not None:
                campaign.donate += value
            else:
                campaign.donate = value

            campaign.save()
            return redirect('donate/', campaign_name=campaign_name)

    else:
        form = CampaignDonateForm
        return render(request, 'campaign_detail.html', {'campaign': campaign, 'form': form})


def donate(request, campaign_name):

    campaign = Campaign.objects.get(campaign_name=campaign_name)

    subject = 'Congratulations!'
    html_message = render_to_string('milestones.html', {'username': campaign.user.username, 'amount': campaign.donate})  # ADD params
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = campaign.user.email
    send_mail(subject, plain_message, from_email, [to_email])

    return render(request, 'donate.html')


def campaign_analytics(request, user_name, campaign_name):
    donors = Donors.objects.filter(campaign=campaign_name)
    cmp = Campaign.objects.filter(campaign_name=campaign_name)
    cmp = cmp.first()

    context = {
        'donors': donors,
        'total': cmp.donate,
        'goal': cmp.goal,
        'pgoal': round((cmp.donate/cmp.goal)*100, 1)
    }

    return render(request, 'campaign_analytics.html', context)
