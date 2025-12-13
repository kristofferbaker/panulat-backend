from django.db import transaction
from blogs.models import *
from django.core.exceptions import ValidationError
from rest_framework import status


@transaction.atomic
def create_blog_post(data, user):
    blog = data.get("blog")
    author = user
    opening_graphic = data.get("opening_graphic")
    title = data.get("title")
    subtitle = data.get("subtitle")
    body = data.get("body")
    locked_to_subscribers = data.get("locked_to_subscribers")

    if blog.blog_author != user:
        raise ValidationError("Not allowed.")

    blog_post = BlogPost.objects.create(
        blog=blog,
        author=author,
        opening_graphic=opening_graphic,
        title=title,
        subtitle=subtitle,
        body=body,
        locked_to_subscribers=locked_to_subscribers,
    )

    return blog_post
