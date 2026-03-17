from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField
from accounts.models import UserProfile, CustomUser
from datetime import datetime


class GlobalExploreFilterSerializer(serializers.Serializer):
    search_query = serializers.CharField(required=False)


class GlobalExploreOutputSerializer(serializers.ModelSerializer):
    blog_author = serializers.SerializerMethodField()
    no_of_subscribers = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def get_blog_author(self, obj):
        return obj.blog_author.username

    def get_no_of_subscribers(self, obj):
        return Subscription.objects.filter(blog=obj).count()


class ListLatestPostsOfSubscribedToBlogsOutputSerializer(serializers.ModelSerializer):
    blog_logo = serializers.SerializerMethodField()
    blog_name = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_blog_logo(self, obj):
        return obj.blog.blog_logo.url

    def get_blog_name(self, obj):
        return obj.blog.blog_name

    def get_author_username(self, obj):
        return obj.blog.blog_author.username

    def get_created_at(self, obj):
        month_to_string = {
            "01": "JAN",
            "02": "FEB",
            "03": "MAR",
            "04": "APR",
            "05": "MAY",
            "06": "JUN",
            "07": "JUL",
            "08": "AUG",
            "09": "SEPT",
            "10": "OCT",
            "11": "NOV",
            "12": "DEC",
        }

        created_at = obj.created_at
        year = datetime.strftime(created_at, "%Y")
        month = month_to_string[datetime.strftime(created_at, "%m")]
        day = datetime.strftime(created_at, "%d")

        return f"{day} {month} {year}"


class StatsOverviewFilterSerializer(serializers.Serializer):
    blog_pk = serializers.IntegerField()
    time_period_filter = serializers.CharField(required=False)


class CreateBlogPostInputSerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    opening_graphic = Base64ImageField(allow_null=True)
    title = serializers.CharField()
    subtitle = serializers.CharField(allow_blank=True, allow_null=True)
    body = serializers.CharField(allow_blank=True, allow_null=True)
    locked_to_subscribers = serializers.BooleanField()
    post_type = serializers.CharField()


class CreateBlogPostOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class ListBlogPostsAccountModeFilterSerializer(serializers.Serializer):
    post_type = serializers.CharField()


class ListBlogPostsAccountModeOutputSerializer(serializers.ModelSerializer):
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    no_of_views = serializers.SerializerMethodField()
    blog_name = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_no_of_likes(self, obj):
        return Like.objects.filter(blog_post=obj).count()

    def get_no_of_comments(self, obj):
        return Comment.objects.filter(blog_post=obj).count()

    def get_no_of_views(self, obj):
        return View.objects.filter(blog_post=obj).count()

    def get_blog_name(self, obj):
        return obj.blog.blog_name


class UpdateBlogPostSerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    opening_graphic = Base64ImageField(required=False)
    title = serializers.CharField()
    subtitle = serializers.CharField()
    body = serializers.CharField()
    locked_to_subscribers = serializers.BooleanField()
    post_type = serializers.CharField()


class UpdateBlogPostOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class BlogPostDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class GetBlogsOfUserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class ListPublishedBlogPostsReadingModeFilterSerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())


class ListPublishedBlogPostsReadingModeOutputSerializer(serializers.ModelSerializer):
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    no_of_views = serializers.SerializerMethodField()
    blog_name = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_no_of_likes(self, obj):
        return Like.objects.filter(blog_post=obj).count()

    def get_no_of_comments(self, obj):
        return Comment.objects.filter(blog_post=obj).count()

    def get_no_of_views(self, obj):
        return View.objects.filter(blog_post=obj).count()

    def get_blog_name(self, obj):
        return obj.blog.blog_name

    def get_author(self, obj):
        class AuthorInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = (
                    "username",
                    "first_name",
                    "last_name",
                )

        return AuthorInlineSerializer(obj.author).data


class BlogPostDetailReadingModeOutputSerializer(serializers.ModelSerializer):
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    no_of_views = serializers.SerializerMethodField()
    blog_name = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_no_of_likes(self, obj):
        return Like.objects.filter(blog_post=obj).count()

    def get_no_of_comments(self, obj):
        return Comment.objects.filter(blog_post=obj).count()

    def get_no_of_views(self, obj):
        return View.objects.filter(blog_post=obj).count()

    def get_blog_name(self, obj):
        return obj.blog.blog_name

    def get_author(self, obj):
        class AuthorInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = (
                    "username",
                    "first_name",
                    "last_name",
                )

        return AuthorInlineSerializer(obj.author).data


class LikeOrRemoveLikeBlogPostInputSerializer(serializers.Serializer):
    blog_post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())


class ListBlogCommentsFilterSerializer(serializers.Serializer):
    blog_post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())


class ListBlogCommentsOutputSerializer(serializers.ModelSerializer):
    commenter = serializers.SerializerMethodField()
    comment_likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_commenter(self, obj):
        class CommenterInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = (
                    "username",
                    "first_name",
                    "last_name",
                )

        return CommenterInlineSerializer(obj.commenter).data

    def get_comment_likes(self, obj):
        return CommentLike.objects.filter(comment=obj).count()


class CreateBlogPostCommentInputSerializer(serializers.Serializer):
    blog_post = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all())
    body = serializers.CharField()


class CreateBlogPostCommentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UpdateBlogPostCommentSerializer(serializers.Serializer):
    body = serializers.CharField()


class UpdateBlogPostCommentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class GetBlogPostCommentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LikeOrRemoveLikeCommentInputSerializer(serializers.Serializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())


class SubscribeToBlogInputSerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())


class GetSubscriptionsFilterSerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())


class GetSubscriptionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class BlogPostsFilterSerializer(serializers.Serializer):
    search_query = serializers.CharField(required=False)


class BlogPostsFilterOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class GetLatestTenBlogPostsofBlogOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class GetProfileOutputSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    blogs = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_user(self, obj):
        class UserInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = [
                    "username",
                    "first_name",
                    "last_name",
                ]

        return UserInlineSerializer(obj.user).data

    def get_blogs(self, obj):
        class BlogInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = Blog
                fields = [
                    "blog_name",
                ]

        blogs = Blog.objects.filter(blog_author=obj.user)

        return BlogInlineSerializer(blogs, many=True).data


class GetPostsTabOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class GetProfileInputSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class GetPostsTabInputSerializer(serializers.Serializer):
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class GetCommentsTabOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class GetCommentsTabInputSerializer(serializers.Serializer):
    commenter = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class GetLikesTabInputSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class GetLikesTabOutputSerializer(serializers.Serializer):
    blog_posts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()


class GetReadsTabInputSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class GetReadsTabOutputSerializer(serializers.ModelSerializer):
    blog_author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def get_blog_author(self, obj):
        class UserInlineSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = [
                    "username",
                    "first_name",
                    "last_name",
                ]

        return UserInlineSerializer(obj.blog_author).data


class EditProfilePictureInputSerializer(serializers.Serializer):
    profile_picture = Base64ImageField()


class EditProfilePictureOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class EditProfileBannerInputSerializer(serializers.Serializer):
    profile_banner = Base64ImageField()


class EditProfileBannerOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
