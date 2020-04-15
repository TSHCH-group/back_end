from django.urls import path
from .views import CompanyCreateView, CompanyDetailView

urlpatterns = [
    path('create/', CompanyCreateView.as_view()),
    path('detail/<int:pk>', CompanyDetailView.as_view(), name='company_detail'),
]
