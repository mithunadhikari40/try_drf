"""lesson1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin', admin.site.urls),
    path('auth-token', obtain_auth_token, name='api_token_auth'),

    # for the docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('student/', include('apps.chapter1.urls'), name="chapter1"),
    path('authentication/', include('apps.authentication.urls'), name="authentication"),
    # default auth route and other rest_framework routes
    path('auth/', include('rest_framework.urls', namespace="rest_framework")),
    path('user/', include('apps.user.urls'), name="user"),
    path('serialization_relation/', include('apps.serialization_relation.urls'), name="serialization_relation"),

]
