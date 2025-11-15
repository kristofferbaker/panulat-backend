from collections import OrderedDict
from math import ceil

from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        pages = count / self.page.paginator.per_page
        pages = ceil(pages)

        return Response(
            OrderedDict(
                [
                    ("count", count),
                    ("pages", pages),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
