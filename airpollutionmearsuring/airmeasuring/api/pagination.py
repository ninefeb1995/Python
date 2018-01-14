from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.LimitOffsetPagination):
    limit_query_param = 'length'
    offset_query_param = 'start'
    template = None

    def get_paginated_response(self, data):
        return Response({
            'recordsTotal': self.count,
            'recordsFiltered': self.count,
            'results': data
        })
