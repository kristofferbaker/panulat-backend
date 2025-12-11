from rest_framework import serializers
from .models import *


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
