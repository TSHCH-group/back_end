from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse
# Create your views here.


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        print(request)
        user_info = {
            'username': request.user.username,
            'is_company': False,
        }
        if hasattr(request.user, 'company'):
            user_info['is_company'] = True
            user_info['company_name'] = request.user.company.company_name

        return JsonResponse(user_info)
