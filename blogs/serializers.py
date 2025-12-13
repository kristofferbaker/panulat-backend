from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField


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

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_blog_logo(self, obj):
        return obj.blog.blog_logo.url

    def get_blog_name(self, obj):
        return obj.blog.blog_name

    def get_author_username(self, obj):
        return obj.blog.blog_author.username


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
    opening_graphic = Base64ImageField()
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
