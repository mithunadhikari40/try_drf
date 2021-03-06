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

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from apps.authentication import views
from .auth_tokenization import AuthTokenization

"""Viewset"""
from rest_framework.routers import DefaultRouter

# creating a router object
router = DefaultRouter()
# register student viewset with router
# model view set
router.register('studentapimodelviewset', views.StudentModelViewSet, basename='studentapimodelviewset')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('<int:pk>', views.student_detail),
    path('', views.student_list),
    # allow the user to create a token using a post request, they need to pass the username and password
    # path('createtoken', obtain_auth_token)
    path('createtoken', AuthTokenization.as_view())

]
