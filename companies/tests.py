from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Company
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart

from posts.views import PostCreateAPIView


def get_image_file(name, ext='jpeg', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)

def get_company_information(pk):
    company = Company.objects.get(pk=pk)
    company_info= {
        'user': f'{company.user}',
        'company_name': f'{company.company_name}',
        'short_description': f'{company.short_description}',
        'description': f'{company.description}',
        'longitude': f'{company.longitude}',
        'latitude': f'{company.latitude}',
    }
    return company_info


class CompanyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        test_user = User.objects.create_user(
            username='testuser', password='abc123')
        test_user.save()
        test_user2 = User.objects.create_user(username='testuser2', password='abc123')
        test_user2.save()

        # Create a company
        test_company = Company.objects.create(
            user=test_user, company_name="Test company name", profile_photo=get_image_file("image2"),
            background_photo=get_image_file("image"), short_description="Test short description",
            description="Test description", longitude=49.000000, latitude=44.000000
        )
        test_company.save()

    def test_company_content(self):
        company_info = get_company_information(1)

        self.assertEqual(company_info['user'], 'testuser')
        self.assertEqual(company_info['company_name'], 'Test company name')
        self.assertEqual(company_info['short_description'], 'Test short description')
        self.assertEqual(company_info['description'], 'Test description')
        self.assertEqual(company_info['longitude'], '49.000000')
        self.assertEqual(company_info['latitude'], '44.000000')

    def test_get_valid_company_detail(self):
        response = self.client.get(reverse('company_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company_detail(self):
        response = self.client.get(reverse('company_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_company_can_create_post(self):
        self.client.login(username='testuser', password='abc123')
        response = self.client.post(reverse('create-post'), follow=True, data={'description': 'Test', 'images': ''})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'Test')

    def test_if_ordinary_user_can_create_post(self):
        self.client.login(username='testuser2', password='abc123')
        response = self.client.post(reverse('create-post'), follow=True, data={'description': 'Test', 'images': ''})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_updating_company_detail_works_properly(self):
        self.client.login(username='testuser', password='abc123')
        data = {
            "company_name": "makememories",
            "profile_photo": "",
            "background_photo": "",
            "short_description": "update testing",
            "description": "update testing",
            "longitude": "123.000000",
            "latitude": "123.123456"
        }
        response = self.client.put(reverse('update_company', kwargs={'pk': 1}), data=encode_multipart(BOUNDARY, data),
                                   content_type=MULTIPART_CONTENT,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company_info = get_company_information(1)
        self.assertEqual(company_info['user'], 'testuser')
        self.assertEqual(company_info['company_name'], 'makememories')
        self.assertEqual(company_info['short_description'], 'update testing')
        self.assertEqual(company_info['description'], 'update testing')
        self.assertEqual(company_info['longitude'], '123.000000')
        self.assertEqual(company_info['latitude'], '123.123456')

    def test_post_list_page(self):
        self.client.login(username='testuser', password='abc123')
        response = self.client.post(reverse('create-post'), follow=True, data={'description': 'Test', 'images': ''})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
