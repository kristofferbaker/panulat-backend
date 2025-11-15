from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from . import models, serializers, services, selectors, pagination


class TestAPI(APIView):
    pass


# API for searching blogs by their name.
class GlobalExploreAPI(APIView):
    filter_serializer_class = serializers.GlobalExploreFilterSerializer
    serializer_class = serializers.GlobalExploreOutputSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination

    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        search_results = selectors.global_search(data=filter_serializer.validated_data)

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(search_results, request)

        # Serialize paginated results.
        serializer = self.serializer_class(paginated_results, many=True)

        # Generate the paginated response with the serialized data.
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)
