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

from apps.user import views

"""Importing jwt token related libs"""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

"""Viewset"""
from rest_framework.routers import DefaultRouter

# creating a router object
router = DefaultRouter()
# register student viewset with router
# model view set
router.register('user', views.StudentModelViewSet, basename='user')
router.register('throttle', views.ThrottleStudentModelViewSet, basename='throttle')

urlpatterns = [
    path('', include(router.urls)),
    # JWT token related routes
    path('gettoken/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refreshtoken/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verifytoken/', TokenVerifyView.as_view(), name="token_verify"),
    path('filter_student/', views.StudentListView.as_view(), name="filter_student"),
    path('add_student/', views.StudentCreateView.as_view(), name="add_student"),
    path('django_filter/', views.StudentListViewDjangoFilter.as_view(), name="django_filter"),

]
