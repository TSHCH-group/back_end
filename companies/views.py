from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import Company
from .serializers import CompanyCreateSerializer, CompanyDetailSerializer
from .permissions import DoesNotHaveCompanyOrDeny


# Create your views here.

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticated, DoesNotHaveCompanyOrDeny,)
    serializer_class = CompanyCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = CompanyDetailSerializer


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self):
        user_info = {
            'username': self.request.user.username,
            'is_company': False,
        }
        if hasattr(self.request.user, 'company'):
            user_info['is_company'] = True
            user_info['company_name'] = self.request.user.company_name

        return JsonResponse(user_info)
