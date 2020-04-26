from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.reverse import reverse

from companies.models import Company
from posts.models import Post
from companies.tests import get_image_file


class FavoriteTest(TestCase):
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

        # Create a post
        test_post = Post.objects.create(company=test_company, description="Test description")
        test_post.save()

    def test_delete_favorite(self):
        self.client.login(username='testuser', password='abc123')
        response = self.client.put(reverse('create-favorite', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 201)
