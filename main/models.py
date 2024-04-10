from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.FloatField(null=True)
    donate = models.FloatField(null=True)
    campaign_logo = models.ImageField(upload_to='company_logos/')

    def __str__(self):
        return self.campaign_name


class Donors(models.Model):
    user = models.CharField(null=True, max_length=100)
    campaign = models.CharField(null=True, max_length=100)
    donate = models.FloatField()
