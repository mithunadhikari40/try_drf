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

from apps.chapter1 import views

"""Viewset"""
from rest_framework.routers import DefaultRouter

# creating a router object
router = DefaultRouter()
# register student viewset with router
router.register('studentapiviewset', views.StudentViewSet, basename='studentapiviewset')

urlpatterns = [
    # for students
    path('<int:pk>', views.student_detail),
    path('', views.student_list),
    path('create', views.create_student),
    path('update', views.update_student),
    path('delete', views.delete_student),
    path('list', views.get_student),
    path('classbasedstudent', views.StudentApiView.as_view()),
    path('genericapilist', views.StudentList.as_view()),
    path('genericapiget/<int:pk>', views.StudentRetrieve.as_view()),
    path('genericapicreate', views.StudentCreate.as_view()),
    path('genericapiupdate/<int:pk>', views.StudentUpdate.as_view()),
    path('genericapidelete/<int:pk>', views.StudentDelete.as_view()),
    path('genericapideleteputget/<int:pk>', views.StudentUpdateAndGetAndDelete.as_view()),
    path('genericapilistcreate', views.StudentListAndCreate.as_view()),

    #router based
    path('viewset/',include(router.urls))

]
