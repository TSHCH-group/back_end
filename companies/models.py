from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


class Company(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    company_name = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)
    background_photo = models.ImageField(upload_to='back_photos', blank=True)
    background_photo_small = models.ImageField(upload_to='back_photos', blank=True)
    short_description = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.background_photo_small = self.background_photo
        instance = super(Company, self).save(*args, **kwargs)
        im = Image.open(self.profile_photo.path)
        im.save(self.profile_photo.path, quality=20, optimize=True)

        im = Image.open(self.background_photo.path)
        im.save(self.background_photo.path, quality=40, optimize=True)

        im = Image.open(self.background_photo_small.path)
        im.save(self.background_photo_small.path, quality=30, optimize=True)

        return instance
