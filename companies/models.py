from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from django.core.files import File


def compress(image, quality=20):
    im_io = BytesIO()
    im = Image.open(image)
    im = im.convert('RGB')
    im.save("test.jpg")
    im.save(im_io, 'JPEG', quality=quality)
    new_image = File(im_io, name=image.name)
    return new_image


class Company(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    company_name = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)
    background_photo = models.ImageField(upload_to='back_photos', blank=True)
    short_description = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.profile_photo = compress(self.profile_photo)
        self.background_photo = compress(self.background_photo, 40)
        super().save(*args, **kwargs)
