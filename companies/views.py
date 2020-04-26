from django.db.models import Q
from rest_framework import generics, permissions
from .models import Company
from .serializers import (
    CompanyCreateUpdateSerializer,
    CompanyDetailSerializer,
    CompanySearchSerializer,
)
from .permissions import DoesNotHaveCompanyOrDeny, IsOwnerOrReadOnly


# Create your views here.

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticated, DoesNotHaveCompanyOrDeny,)
    serializer_class = CompanyCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = CompanyDetailSerializer


class CompanySearchView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CompanySearchSerializer

    def get_queryset(self):
        queryset_list = Company.objects.all().order_by('company_name')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(company_name__contains=query)
            ).distinct().order_by('company_name')
        return queryset_list


class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
