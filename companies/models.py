from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Company(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete = models.CASCADE,
        primary_key = True,
    )
    company_name = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)
    background_photo = models.ImageField(upload_to='back_photos', blank=True)
    short_description = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.company_name