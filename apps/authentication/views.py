import io
from django.shortcuts import render

"""Modal view set, where it provides all of the actions and other method"""

from .models import Student
from .serializers import StudentSerializer

"""Implementing basic auth, on this, the user needs to pass the username and password on every request"""

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Model Object - Single Student Data
from rest_framework import viewsets


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # user needs to pass username and password to authenticate
    authentication_classes = [BasicAuthentication]
    # once the user is authenticated, they can do pretty much anything regardless of them being normal user,
    # staff or super admin
    permission_classes = [IsAuthenticated]
    # once the user is authenticated, they can do pretty much anything if they are staff
    # permission_classes = [IsAdminUser]
