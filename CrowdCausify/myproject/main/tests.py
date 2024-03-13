from django.test import TestCase
from django.urls import reverse


class MainTest(TestCase):
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

    def test_login_success(self):
        login_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), login_data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue('_auth_user_id' in self.client.session)
