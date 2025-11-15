from rest_framework import serializers
from .models import Blog, Subscription


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
