from django.urls import path
from .views import (
    CompanyCreateView,
    CompanyDetailView,
    CompanySearchView,
    CompanyUpdateView,
)

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='create_company'),
    path('update/<int:pk>/', CompanyUpdateView.as_view(), name='update_company'),
    path('detail/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('search/', CompanySearchView.as_view(), name='search'),
]
