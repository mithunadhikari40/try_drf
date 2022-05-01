from rest_framework.authentication import BaseAuthentication

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class CustomNumberPagination(PageNumberPagination):
    """Modify the default pagination attributes provided by rest_framework"""
    page_size = 3
    """Transform the page param in the query
    Transfer http://localhost:7000/user/paginate_students/?p=2
    from http://localhost:7000/user/paginate_students/?page=2"""
    page_query_param = 'p'
    """Defines whether the client can request for the page size and what param to use to do so, will override our 
    page_size attribute. Url becomes http://localhost:7000/user/paginate_students/?p=1&pagesize=5 """
    page_size_query_param = 'pagesize'
    """Defines what is the max value of page_size_query_param would be, meaning one page will not return more that 
    what is provided here, does not interrupt page_size though"""
    max_page_size = 2
    """http://localhost:7000/user/paginate_students/?p=last will return the last pagination"""
    # defines what the ?p=last be, e.g ?p=end
    # http://localhost:7000/user/paginate_students/?p=end
    last_page_strings = 'end'

    """Override the default implementation of pagination. The default looks like this:
        {
        "count": 4,
        "next": null,
        "previous": "http://localhost:7000/user/paginate_students/",
        "results": [
            {
                "id": 5,
                "name": "one",
                "roll": 233,
                "city": "pokhara",
                "by": "autocreatedtoken"
            }
        ]
        }
    """

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'data': data,
            'something': 'something else'
        })

    """Now the response becomes something like this
        {
        "next": null,
        "previous": "http://localhost:7000/user/paginate_students/",
        "count": 4,
        "data": [
            {
                "id": 5,
                "name": "one",
                "roll": 233,
                "city": "pokhara",
                "by": "autocreatedtoken"
            }
        ],
        "something": "something else"
        }
    """


"""Pagination with offset and limit
The url becomes something like this http://localhost:7000/user/limit_offset_students/?limit=2
http://localhost:7000/user/limit_offset_students/?limit=2&offset=1"""


class CustomLimitOffsetPagination(LimitOffsetPagination):
    # default limit, can be override by limit param
    default_limit = 1
    # modify the limit param  http://localhost:7000/user/limit_offset_students/?l=2&offset=1"""
    limit_query_param = 'l'
    # modify the offset param  http://localhost:7000/user/limit_offset_students/?limit=2&o=1"""
    offset_query_param = 'o'
    # limit the max value of limit param
    max_limit = 3


"""Pagination with cursor
The url becomes something like this http://localhost:7000/user/limit_offset_students/?limit=2
http://localhost:7000/user/limit_offset_students/?limit=2&offset=1"""


class CustomCursorPagination(CursorPagination):
    """Modify the default pagination attributes provided by rest_framework"""
    page_size = 3
    "cursor query param, defaults to cursor"
    cursor_query_param = 'c'
    """the field on which the cursor will be ordered upon, defaults to created, so the pagination will be according 
    to created_date and first added item will be there first. This field is recommended be a timestamp so that the 
    ordering is consistent. If we do not provide it and if our model class does not have created field, it throws an 
    error ordering = -created will reverse the ordering """
    # ordering = '-created_at'
    ordering = 'created_at'
