"""makememories URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.views import get_swagger_view
from allauth.account.views import confirm_email


API_TITLE = 'Make Memories'
API_DESCRIPTION = 'This site is for tourists and tour companies'
schema_view = get_swagger_view(title=API_TITLE)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', include('companies.urls')),
    path('favorite/', include('favorites.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('posts.urls'), name='home'),
    path('login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('docs/', include_docs_urls(title=API_TITLE)),
    path('user/', include('userinformation.urls')),
    path('swagger-docs/', schema_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
