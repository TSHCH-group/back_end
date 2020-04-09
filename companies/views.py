from rest_framework import generics
from rest_framework import permissions
from .models import Company
from .serializers import CompanySerializerForCreate
from .permissions import DoesNotHaveCompanyOrDeny
# Create your views here.

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticated, DoesNotHaveCompanyOrDeny, )
    serializer_class = CompanySerializerForCreate

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)