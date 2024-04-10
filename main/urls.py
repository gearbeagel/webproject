from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:user_name>', views.profile, name='profile'),
    path('campaign/', views.create_campaign, name='campaign'),
    path('campaign/view/<str:campaign_name>/', views.campaign_detail, name='campaign_detail'),
    path('profile/<str:user_name>/<str:campaign_name>/settings', views.campaign_analytics, name='campaign_settings'),
    path('campaign/view/<str:campaign_name>/donate/', views.donate, name='donate'),
    path('campaign/success_page/', views.success_page),
]
