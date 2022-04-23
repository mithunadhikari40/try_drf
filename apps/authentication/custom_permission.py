from django.db import models
from rest_framework.permissions import BasePermission

from apps.utils.timestamp.models import TimeStamp


class MyCustomPermission(BasePermission):
    """We have to override at least one of has_permission or has_object_permission method, when returned True,
    the permission will be allowed else not """

    def has_permission(self, request, view):
        # only allowing if the request is get request
        if request.method == 'GET':
            return True
        return False

    """Useful when we want to verify that this either of update, or delete is being made by the author"""

    def has_object_permission(self, request, view, obj):
        return True
