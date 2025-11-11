from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser


class Blog(models.Model):
    blog_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    blog_name = models.CharField(max_length=255, null=True)
    blog_banner = models.ImageField(blank=True, null=True)
    blog_logo = models.ImageField(blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def create_or_update_blog(sender, instance, created, **kwargs):
        Blog.objects.get_or_create(blog_author=instance)


class Subscription(models.Model):
    email = models.CharField(
        max_length=255
    )  # email can only be subscribed once to a blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=False)


class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now())
    opening_graphic = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    lockedToSubscribers = models.BooleanField(default=False)


class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())


class Like(models.Model):  # One like is alloted per user for a single post.
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())


class View(models.Model):  # Needs to be unique. One view to an IP address or user.
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )


class Quote(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
