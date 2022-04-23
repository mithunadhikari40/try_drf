from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

"""Modal view set, where it provides all of the actions and other method"""

"""Implementing basic auth, on this, the user needs to pass the username and password on every request"""

# Model Object - Single Student Data
from rest_framework import viewsets

# Model Object - Single Student Data
from .models import Student
from .serializers import StudentSerializer


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
