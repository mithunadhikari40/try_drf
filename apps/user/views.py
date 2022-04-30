from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import Throttled
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .custom_authentication import CustomAuthentication

"""Modal view set, where it provides all of the actions and other method"""

"""Implementing basic auth, on this, the user needs to pass the username and password on every request"""

# Model Object - Single Student Data
from rest_framework import viewsets

# Model Object - Single Student Data
from .models import Student
from .serializers import StudentSerializer

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import SessionAuthentication


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    # authentication_classes = [CustomAuthentication]


"""Example of throttling"""

from .custom_throttling import CustomRateThrottle

from rest_framework.throttling import ScopedRateThrottle


class ThrottleStudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [AnonRateThrottle, CustomRateThrottle]
    throttle_classes = [AnonRateThrottle, ScopedRateThrottle]
    # defining the throttle scope rates
    throttle_scope = 'throttle_view'

    """Custom message for throttling"""

    def throttled(self, request, wait):
        raise Throttled(
            detail={
                "message": "request limit exceeded",
                "availableIn": f"{wait} seconds",
                "method": request.method,
                "throttleType": self.throttle_scope
            }
        )


class StudentListView(ListAPIView):
    queryset = Student.objects.all()

    """One way to filter out"""
    # queryset = Student.objects.filter(name='Asuma')
    serializer_class = StudentSerializer
    """Overriding what default queryset returns"""

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(by=user)

class StudentListViewDjangoFilter(ListAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentSerializer


class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
