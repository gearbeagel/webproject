from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Додаємо поле для зв'язку з користувачем
    campaign_name = models.CharField(max_length=100)
    description = models.TextField()
    campaign_logo = models.ImageField(upload_to='company_logos/')

    def __str__(self):
        return self.campaign_name
