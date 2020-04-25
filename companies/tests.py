from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Company
from io import BytesIO
from PIL import Image
from django.core.files.base import File


def get_image_file(name, ext='jpeg', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class CompanyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        test_user = User.objects.create_user(
            username='testuser', password='abc123')
        test_user.save()

        # Create a company
        test_company = Company.objects.create(
            user=test_user, company_name="Test company name", profile_photo=get_image_file("image2"),
            background_photo=get_image_file("image"), short_description="Test short description",
            description="Test description", longitude=49.000000, latitude=44.000000
        )
        test_company.save()

    def test_company_content(self):
        company = Company.objects.get(user_id=1)
        user = f'{company.user}'
        company_name = f'{company.company_name}'
        short_description = f'{company.short_description}'
        description = f'{company.description}'
        longitude = f'{company.longitude}'
        latitude = f'{company.latitude}'

        self.assertEqual(user, 'testuser')
        self.assertEqual(company_name, 'Test company name')
        self.assertEqual(short_description, 'Test short description')
        self.assertEqual(description, 'Test description')
        self.assertEqual(longitude, '49.000000')
        self.assertEqual(latitude, '44.000000')

    def test_get_valid_company_detail(self):
        response = self.client.get(reverse('company_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company_detail(self):
        response = self.client.get(reverse('company_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
