from rest_framework import serializers
from .models import Company
from django.contrib.auth import get_user_model


class CompanySerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description']