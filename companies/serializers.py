from rest_framework import serializers
from .models import Company
from django.contrib.auth import get_user_model


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description', 'longitude',
                  'latitude']


class CompanyDetailSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description',
                  'longitude', 'latitude', 'posts', 'is_owner']

    def get_is_owner(self, obj):
        if self.context['request'].user == obj.user:
            return True
        return False


class CompanyHyperLinkSerializer(serializers.HyperlinkedRelatedField):
    company = serializers.HyperlinkedRelatedField(read_only=True, view_name='company_detail')

    class Meta:
        model = Company
        fields = ['company', ]
