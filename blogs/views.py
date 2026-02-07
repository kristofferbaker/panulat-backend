from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from . import models, serializers, services, selectors, pagination, permissions
from rest_framework import serializers as rest_serializers
from django.http import Http404
from accounts.models import UserProfile, CustomUser


class GlobalExploreAPI(APIView):
    filter_serializer_class = serializers.GlobalExploreFilterSerializer
    serializer_class = serializers.GlobalExploreOutputSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("search_query", OpenApiTypes.STR),
        ],
        operation_id="Global explore of blogs",
        description="API for searching blogs by their name.",
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


class ListLatestPostsOfSubscribedToBlogsAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListLatestPostsOfSubscribedToBlogsOutputSerializer
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("search_query", OpenApiTypes.STR),
        ],
        operation_id="List latest posts of subscribed to blogs",
        description="API for getting the list of the latest blog posts of blogs a user has subscribed to.",
    )
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
        operation_id="Get the stats of a user's blog",
        description="API for getting the number of views and subscribers a user's blog has",
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
        operation_id="Create a blog post",
        description="API for a user to create a blog post for their blog",
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
        operation_id="Get the blogs posts of a user's blog",
        description="API for allowing a user to view the blog posts of their blog in account mode",
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        blog_posts = selectors.get_blog_posts_account_mode(
            data=filter_serializer.validated_data, user=request.user
        ).order_by("-created_at")

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

    @extend_schema(
        operation_id="Update a blog post",
        description="API for user's to update a specific blog post of their blog",
    )
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
        operation_id="Get a blog post",
        description="API for viewing the details of a blog post",
    )
    def get(self, request, pk):
        blog_post = models.BlogPost.objects.get(pk=pk, author=request.user)

        output = self.output_serializer(blog_post).data

        return Response(output, status=status.HTTP_200_OK)


class SoftDeleteBlogPostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        operation_id="Soft delete a blog post",
    )
    def delete(self, request, pk):
        blog_post = models.BlogPost.objects.get(pk=pk, author=request.user)
        blog_post.post_type = "DE"
        blog_post.save()

        return Response(status=status.HTTP_200_OK)


class GetBlogsOfUserAPI(APIView):
    permission_classes = (IsAuthenticated,)
    output_serializer = serializers.GetBlogsOfUserOutputSerializer

    @extend_schema(
        responses=serializers.GetBlogsOfUserOutputSerializer,
        operation_id="List blogs of a user",
    )
    def get(self, request):
        blogs = models.Blog.objects.filter(blog_author=request.user).order_by(
            "-created_at"
        )

        output = self.output_serializer(blogs, many=True).data

        return Response(output, status=status.HTTP_200_OK)


class ListPublishedBlogPostsReadingModeAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer_class = (
        serializers.ListPublishedBlogPostsReadingModeFilterSerializer
    )
    serializer_class = serializers.ListPublishedBlogPostsReadingModeOutputSerializer
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("post_type", OpenApiTypes.STR),
        ],
        responses=serializers.ListPublishedBlogPostsReadingModeOutputSerializer,
        operation_id="List published blog posts for a reader",
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        blog_posts = selectors.get_published_blog_posts_reading_mode(
            data=filter_serializer.validated_data
        ).order_by("-created_at")

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(blog_posts, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


class BlogPostDetailReadingModeAPI(APIView):
    permission_classes = (AllowAny,)
    output_serializer = serializers.BlogPostDetailReadingModeOutputSerializer

    @extend_schema(
        responses=serializers.BlogPostDetailReadingModeOutputSerializer,
        operation_id="Get the specific blog post for a reader",
    )
    def get(self, request, pk):
        blog_post = models.BlogPost.objects.get(pk=pk, post_type="PU")

        output = self.output_serializer(blog_post).data

        return Response(output, status=status.HTTP_200_OK)


class LikeOrRemoveLikeBlogPostAPI(APIView):
    permission_classes = (IsAuthenticated,)
    input_serializer_class = serializers.LikeOrRemoveLikeBlogPostInputSerializer

    @extend_schema(
        request=serializers.LikeOrRemoveLikeBlogPostInputSerializer,
        operation_id="Like or unlike a blog post",
    )
    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data

        services.like_or_remove_like_blog_post(data, user=request.user)

        return Response(status=status.HTTP_200_OK)


class ListBlogPostCommentsAPI(APIView):
    filter_serializer_class = serializers.ListBlogCommentsFilterSerializer
    serializer_class = serializers.ListBlogCommentsOutputSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("blog_post", OpenApiTypes.INT),
        ],
        operation_id="List comments of a blog post",
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        comments = selectors.get_blog_post_comments(
            data=filter_serializer.validated_data
        )

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(comments, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


class CreateBlogPostCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    input_serializer_class = serializers.CreateBlogPostCommentInputSerializer
    output_serializer_class = serializers.CreateBlogPostCommentOutputSerializer

    @extend_schema(
        request=serializers.CreateBlogPostCommentInputSerializer,
        responses=serializers.CreateBlogPostCommentOutputSerializer,
        operation_id="Create a blog post comment",
    )
    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data

        comment = services.create_blog_post_comment(data, user=request.user)

        output = self.output_serializer_class(comment).data

        return Response(output, status=status.HTTP_200_OK)


class DeleteBlogPostCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        operation_id="Delete a blog post comment",
    )
    def delete(self, request, pk):
        comment = models.Comment.objects.get(pk=pk, commenter=request.user)
        comment.delete()

        return Response(status=status.HTTP_200_OK)


class UpdateBlogPostCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateBlogPostCommentSerializer
    output_serializer = serializers.UpdateBlogPostCommentOutputSerializer

    @extend_schema(
        operation_id="Update a blog post comment",
    )
    def patch(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_blog_post_comment = services.update_blog_post_comment(
            data=serializer.validated_data, pk=pk, user=request.user
        )

        data = self.output_serializer(updated_blog_post_comment).data

        return Response(data, status=status.HTTP_200_OK)


class GetBlogPostCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    output_serializer = serializers.GetBlogPostCommentOutputSerializer

    @extend_schema(
        responses=serializers.GetBlogPostCommentOutputSerializer,
        operation_id="Get a blog post comment",
    )
    def get(self, request, pk):
        try:
            comment = models.Comment.objects.get(pk=pk, commenter=request.user)

            output = self.output_serializer(comment).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class LikeOrRemoveLikeCommentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    input_serializer_class = serializers.LikeOrRemoveLikeCommentInputSerializer

    @extend_schema(
        request=serializers.LikeOrRemoveLikeCommentInputSerializer,
        operation_id="Like or unlike a blog post comment",
    )
    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data

        services.like_or_remove_like_comment(data, user=request.user)

        return Response(status=status.HTTP_200_OK)


class SubscribeToBlogAPI(APIView):
    permission_classes = (IsAuthenticated,)
    input_serializer_class = serializers.SubscribeToBlogInputSerializer

    @extend_schema(
        request=serializers.SubscribeToBlogInputSerializer,
        operation_id="Subscribe to a blog",
    )
    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data

        services.subscribe_to_blog(data, user=request.user)

        return Response(status=status.HTTP_200_OK)


class UnsubscribeToBlogAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=serializers.SubscribeToBlogInputSerializer,
        operation_id="Unsubscribe to a blog",
    )
    def patch(self, request, pk):
        try:
            subscription = models.Subscription.objects.get(pk=pk)
            subscription.is_active = False
            subscription.save()

            return Response(status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class GetSubscriptionAPI(APIView):
    permission_classes = (IsAuthenticated,)
    filter_serializer = serializers.GetSubscriptionsFilterSerializer
    output_serializer = serializers.GetSubscriptionOutputSerializer

    @extend_schema(
        responses=serializers.GetSubscriptionOutputSerializer,
        operation_id="Get a subscription",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            subscription = selectors.get_subscription(
                data=filter_serializer.validated_data, user=request.user
            )

            if subscription == None:
                output = False
            else:
                output = self.output_serializer(subscription).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class FilterBlogPostsofBlogAPI(APIView):
    filter_serializer_class = serializers.BlogPostsFilterSerializer
    serializer_class = serializers.BlogPostsFilterOutputSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("search_query", OpenApiTypes.STR),
        ],
        operation_id="Search blog posts of a blog",
    )
    def get(self, request):
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        search_results = selectors.filter_blog_posts(
            data=filter_serializer.validated_data
        )

        # Paginate records.
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(search_results, request)
        serializer = self.serializer_class(paginated_results, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)


class GetLatestTenBlogPostsofBlogAPI(APIView):
    permission_classes = (AllowAny,)
    output_serializer = serializers.GetLatestTenBlogPostsofBlogOutputSerializer

    @extend_schema(
        responses=serializers.GetLatestTenBlogPostsofBlogOutputSerializer,
        operation_id="Get latest ten blog posts of a blog",
    )
    def get(self, request, pk):
        try:
            # Get latest published 10 blog posts of specific blog.
            blog = models.Blog.objects.get(pk=pk)
            latest_ten_blog_posts = models.BlogPost.objects.filter(
                blog=blog, post_type="PU"
            ).order_by("-created_at")[:10]

            output = self.output_serializer(latest_ten_blog_posts, many=True).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class GetProfileAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer = serializers.GetProfileInputSerializer
    output_serializer = serializers.GetProfileOutputSerializer

    @extend_schema(
        responses=serializers.GetProfileOutputSerializer,
        operation_id="Get a user's profile",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)
            data = filter_serializer.validated_data

            profile = UserProfile.objects.filter(user=data["user"]).first()

            output = self.output_serializer(profile).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class PostsTabAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer = serializers.GetPostsTabInputSerializer
    output_serializer = serializers.GetPostsTabOutputSerializer

    @extend_schema(
        responses=serializers.GetPostsTabOutputSerializer,
        operation_id="Posts tab",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)
            data = filter_serializer.validated_data

            posts = models.BlogPost.objects.filter(
                author=data["author"], post_type="PU"
            ).order_by("-created_at")

            output = self.output_serializer(posts, many=True).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class CommentsTabAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer = serializers.GetCommentsTabInputSerializer
    output_serializer = serializers.GetCommentsTabOutputSerializer

    @extend_schema(
        responses=serializers.GetCommentsTabOutputSerializer,
        operation_id="Comments tab",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)
            data = filter_serializer.validated_data

            comments = models.Comment.objects.filter(
                commenter=data["commenter"]
            ).order_by("-created_at")

            output = self.output_serializer(comments, many=True).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class LikesTabAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer = serializers.GetLikesTabInputSerializer

    @extend_schema(
        operation_id="Likes tab",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)
            data = filter_serializer.validated_data

            comment_likes = models.CommentLike.objects.filter(user=data["user"])

            class CommentInlineSerializer(rest_serializers.ModelSerializer):
                commenter = rest_serializers.SerializerMethodField()
                profile = rest_serializers.SerializerMethodField()

                class Meta:
                    model = models.Comment
                    fields = "__all__"

                def get_commenter(self, obj):
                    class UserInlineSerializer(rest_serializers.ModelSerializer):
                        class Meta:
                            model = CustomUser
                            fields = [
                                "username",
                                "first_name",
                                "last_name",
                            ]

                    return UserInlineSerializer(obj.commenter).data

                def get_profile(self, obj):
                    class UserProfileInlineSerializer(rest_serializers.ModelSerializer):
                        class Meta:
                            model = UserProfile
                            fields = [
                                "profile_picture",
                            ]

                    user_profile = UserProfile.objects.filter(user=obj.commenter)

                    return UserProfileInlineSerializer(user_profile).data

            liked_comments = []

            for comment_like in comment_likes:
                comment = comment_like.comment

                serialized_comment = CommentInlineSerializer(comment).data

                liked_comments.append(serialized_comment)

            class PostsInlineSerializer(rest_serializers.ModelSerializer):
                blog = rest_serializers.SerializerMethodField()
                author = rest_serializers.SerializerMethodField()

                class Meta:
                    model = models.BlogPost
                    fields = "__all__"

                def get_blog(self, obj):
                    class BlogInlineSerializer(rest_serializers.ModelSerializer):
                        class Meta:
                            model = models.Blog
                            fields = [
                                "blog_name",
                            ]

                    return BlogInlineSerializer(obj.blog).data

                def get_author(self, obj):
                    class UserInlineSerializer(rest_serializers.ModelSerializer):
                        class Meta:
                            model = CustomUser
                            fields = [
                                "username",
                                "first_name",
                                "last_name",
                            ]

                    return UserInlineSerializer(obj.author).data

            post_likes = models.Like.objects.filter(user=data["user"])

            liked_posts = []

            for post_like in post_likes:
                post = post_like.blog_post

                serialized_post = PostsInlineSerializer(post).data

                liked_posts.append(serialized_post)

            output = {"liked_comments": liked_comments, "liked_posts": liked_posts}

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class ReadsTabAPI(APIView):
    permission_classes = (AllowAny,)
    filter_serializer = serializers.GetReadsTabInputSerializer
    output_serializer = serializers.GetReadsTabOutputSerializer

    @extend_schema(
        responses=serializers.GetReadsTabOutputSerializer,
        operation_id="Reads tab",
    )
    def get(self, request):
        try:
            filter_serializer = self.filter_serializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)
            data = filter_serializer.validated_data

            subscriptions = models.Subscription.objects.filter(subscriber=data["user"])

            subscribed_to_blogs = []

            for subscription in subscriptions:
                blog = subscription.blog

                subscribed_to_blogs.append(blog)

            output = self.output_serializer(subscribed_to_blogs, many=True).data

            return Response(output, status=status.HTTP_200_OK)
        except:
            raise Http404("Something went wrong.")


class EditProfilePictureAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EditProfilePictureInputSerializer
    output_serializer = serializers.EditProfilePictureOutputSerializer

    @extend_schema(
        operation_id="Edit profile picture",
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_profile = services.edit_profile_picture(
            data=serializer.validated_data, user=request.user
        )

        data = self.output_serializer(updated_profile).data

        return Response(data, status=status.HTTP_200_OK)


class EditProfileBannerAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EditProfileBannerInputSerializer
    output_serializer = serializers.EditProfileBannerOutputSerializer

    @extend_schema(
        operation_id="Edit profile banner",
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_profile = services.edit_profile_banner(
            data=serializer.validated_data, user=request.user
        )

        data = self.output_serializer(updated_profile).data

        return Response(data, status=status.HTTP_200_OK)
