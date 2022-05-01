from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import Throttled
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .custom_authentication import CustomAuthentication
from .custom_pagination import CustomNumberPagination, CustomLimitOffsetPagination, CustomCursorPagination

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


from django_filters.rest_framework import DjangoFilterBackend


class StudentListViewDjangoFilter(ListAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentSerializer
    """Not needed if this is mentioned in settings.py"""
    # filter_backends = [DjangoFilterBackend]

    filterset_fields = ['city', 'roll']


"Simple search with django admin search, search is available for text fields only"


class StudentListViewSearch(ListAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentSerializer
    filter_backends = [SearchFilter]

    # search_fields = ['^city', '^name']
    # search_fields = ['=city', '=name']
    search_fields = ['city', 'name']
    # search_fields = ['@city']

    """Search options:"""
    # http://localhost:7000/user/search_students/?search=as
    # ^ - starts with
    # = - full text search
    # $ - regex search
    # nothing then contains method will be applied


"""Simple order by. Ordering fields available are list of fields that you want the response to be ordered with
Optionally if we need to order by every field we can specify something like this
ordering_fields='__all__'
The url to order by roll ascending is 
http://localhost:7000/user/order_students/?ordering=roll
The url to order by roll descending is 
http://localhost:7000/user/order_students/?ordering=-roll"""


class StudentListViewOrder(ListAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentSerializer
    filter_backends = [OrderingFilter]

    ordering_fields = ['city', 'name', 'roll']
    # ordering_fields ='__all__'


"""Pagination that takes global settings"""

# class StudentListViewPagination(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     """When we need to set attributes in PageNumberPagination class, we are ought to create a custom implementaion of
#     it and then override attributes there """
#     # pagination_class = PageNumberPagination


"""Pagination with custom page numer attributes"""


class StudentListViewPagination(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomNumberPagination


"""Pagination with custom offset and limit attributes"""


class StudentListViewLimitOffsetPagination(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomLimitOffsetPagination


"""Pagination with cursor attributes"""


class StudentListViewCursorPagination(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomCursorPagination


class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
