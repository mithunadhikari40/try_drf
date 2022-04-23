import io

from rest_framework.permissions import IsAuthenticated

from .custom_permission import MyCustomPermission

"""Modal view set, where it provides all of the actions and other method"""

"""Implementing basic auth, on this, the user needs to pass the username and password on every request"""

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view

# Model Object - Single Student Data
from rest_framework import viewsets

# Model Object - Single Student Data
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt


class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # user needs to pass username and password to authenticate
    # authentication_classes = [BasicAuthentication]
    # uses session auth, need to use valid_csrf for unsafe http methods,such as put, patch, post and delete
    # authentication_classes = [SessionAuthentication]
    # token authentication
    authentication_classes = [TokenAuthentication]

    # once the user is authenticated, they can do pretty much anything regardless of them being normal user,
    # staff or super admin
    # permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, DjangoModelPermissions,
    #                       DjangoModelPermissionsOrAnonReadOnly,DjangoObjectPermissions]
    # permission_classes = [IsAuthenticated]
    # once the user is authenticated, they can do pretty much anything if they are staff
    # permission_classes = [IsAdminUser]
    """custom permission example"""
    permission_classes = [MyCustomPermission]


"""Permission and Authentication on function based views"""


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def student_detail(req, pk):
    stu = Student.objects.get(id=pk)
    serializer = StudentSerializer(stu)
    return JsonResponse(serializer.data)


# querty set - all student list

"""Permission and Authentication on function based views"""


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def student_list(req):
    stu = Student.objects.all()
    serializer = StudentSerializer(stu, many=True)
    json = JSONRenderer().render(serializer.data)
    return HttpResponse(json, content_type='application/json')
