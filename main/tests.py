from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Campaign


class MainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')
        self.client.login(username='testuser', password='TestPassword123')
        self.campaign = Campaign.objects.create(campaign_name='Test Campaign', user=self.user)

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_profile_view_authenticated_user(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'Test Campaign')

    def test_create_campaign1(self):
        data = {
            'campaign_name': 'Test Campaign',
            'description': 'This is a test campaign.',
            'campaign_icon': None,
        }
        response = self.client.post(reverse('create_campaign'), data)
        self.assertEqual(response.status_code, 302)

    def test_create_campaign2(self):
        data = {
            'campaign_name': 'My Campaign',
            'description': 'My campaign is beautiful.',
            'campaign_icon': None,
        }
        response = self.client.post(reverse('create_campaign'), data)
        self.assertEqual(response.status_code, 302)

