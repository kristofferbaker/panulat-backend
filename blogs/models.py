from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import django

from accounts.models import CustomUser


class Blog(models.Model):
    blog_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    blog_name = models.CharField(max_length=255, null=True)
    blog_banner = models.ImageField(blank=True, null=True)
    blog_logo = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    @receiver(post_save, sender=CustomUser)
    def create_blog(sender, instance, created, **kwargs):
        blog = Blog.objects.filter(blog_author=instance).first()

        if blog == None:
            Blog.objects.create(blog_author=instance)


# Only logged-in users can subscribe.
# User can only subscribe once to a blog.
class Subscription(models.Model):
    email = models.CharField(max_length=255)
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )  # Use if reader IS logged in.
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    is_active = models.BooleanField(default=True)


class BlogPost(models.Model):
    class PostType(models.TextChoices):
        PUBLISHED = "PU"
        SCHEDULED = "SCH"
        DRAFTS = "DR"
        DELETED = "DE"

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    opening_graphic = models.ImageField(null=True, upload_to="images/")
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    locked_to_subscribers = models.BooleanField(default=False)
    post_type = models.CharField(choices=PostType, max_length=255, default="DR")


class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    body = models.TextField()


class Like(models.Model):  # One like is alloted per user for a single post.
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)


class View(models.Model):  # Needs to be unique. One view to an IP address or user.
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(default=django.utils.timezone.now)


class Quote(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()


class CommentLike(models.Model):  # One like is alloted per user for a single comment.
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
