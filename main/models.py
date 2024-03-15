from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Campaign(models.Model):
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/')

    def __str__(self):
        return self.company_name
