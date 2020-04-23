from django.urls import path
from .views import (
    CompanyCreateView,
    CompanyDetailView,
    CompanySearchView,
    UserDetailView,
)

urlpatterns = [
    path('create/', CompanyCreateView.as_view()),
    path('detail/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('', UserDetailView.as_view(), name='user_detail'),
    path('search/', CompanySearchView.as_view(), name='search'),
]
