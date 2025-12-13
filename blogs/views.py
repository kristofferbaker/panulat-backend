from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from . import models, serializers, services, selectors, pagination, permissions
from rest_framework import serializers as rest_serializers


# API for searching blogs by their name.
class GlobalExploreAPI(APIView):
    filter_serializer_class = serializers.GlobalExploreFilterSerializer
    serializer_class = serializers.GlobalExploreOutputSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("search_query", OpenApiTypes.STR),
        ],
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        search_results = selectors.global_search(data=filter_serializer.validated_data)

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(search_results, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


# API for getting the list of the latest blog posts of blogs a user has subscribed to.
class ListLatestPostsOfSubscribedToBlogsAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListLatestPostsOfSubscribedToBlogsOutputSerializer
    pagination_class = pagination.PageNumberPagination

    def get(self, request):
        latest_blog_posts = selectors.get_latest_blog_posts_of_subscribed_to_blogs(
            user=self.request.user
        )

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(latest_blog_posts, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


class StatsOverviewAPI(APIView):
    filter_serializer_class = serializers.StatsOverviewFilterSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter("blog_pk", OpenApiTypes.INT),
            OpenApiParameter("time_period_filter", OpenApiTypes.STR),
        ],
        responses=inline_serializer(
            "StatsOverviewOutputSerializer",
            {
                "total_views": rest_serializers.IntegerField(),
                "total_subscribers": rest_serializers.IntegerField(),
            },
        ),
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        stats = selectors.get_stats(
            data=filter_serializer.validated_data, user=request.user
        )

        return Response(stats, status=status.HTTP_200_OK)


class CreateBlogPostAPI(APIView):
    permission_classes = (IsAuthenticated,)
    input_serializer_class = serializers.CreateBlogPostInputSerializer
    output_serializer_class = serializers.CreateBlogPostOutputSerializer

    @extend_schema(
        request=serializers.CreateBlogPostInputSerializer,
        responses=serializers.CreateBlogPostOutputSerializer,
    )
    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data

        blog_post = services.create_blog_post(data, user=request.user)

        output = self.output_serializer_class(blog_post).data

        return Response(output, status=status.HTTP_200_OK)


class ListBlogPostsAccountModeAPI(APIView):
    permission_classes = (IsAuthenticated,)
    filter_serializer_class = serializers.ListBlogPostsAccountModeFilterSerializer
    serializer_class = serializers.ListBlogPostsAccountModeOutputSerializer
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("post_type", OpenApiTypes.STR),
        ],
        responses=serializers.ListBlogPostsAccountModeOutputSerializer,
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        blog_posts = selectors.get_blog_posts_account_mode(
            data=filter_serializer.validated_data, user=request.user
        )

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(blog_posts, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


class UpdateBlogPostAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateBlogPostSerializer
    output_serializer = serializers.UpdateBlogPostOutputSerializer

    def patch(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_blog_post = services.update_blog_post(
            data=serializer.validated_data, pk=pk, user=request.user
        )

        data = self.output_serializer(updated_blog_post).data

        return Response(data, status=status.HTTP_200_OK)


class BlogPostDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)
    output_serializer = serializers.BlogPostDetailOutputSerializer

    @extend_schema(
        responses=serializers.BlogPostDetailOutputSerializer,
    )
    def get(self, request, pk):
        blog_post = models.BlogPost.get(pk=pk, author=request.user)

        output = self.output_serializer(blog_post).data

        return Response(output, status=status.HTTP_200_OK)


class SoftDeleteBlogPostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        blog_post = models.BlogPost.get(pk=pk, author=request.user)
        blog_post.post_type = "DE"
        blog_post.save()

        return Response(status=status.HTTP_200_OK)
