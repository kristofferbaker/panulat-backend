from blogs.models import Blog
from accounts.models import CustomUser
from django.db.models import Q


def global_search(data):
    search_query = data["search_query"]

    matching_blogs = Blog.objects.filter(blog_name__icontains=search_query)

    return matching_blogs
