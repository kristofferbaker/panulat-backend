from django.contrib import admin
from .models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "blog_author",
        "blog_name",
        "blog_banner",
        "blog_logo",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "subscriber",
        "blog",
        "created_at",
        "is_active",
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "blog",
        "author",
        "created_at",
        "opening_graphic",
        "title",
        "subtitle",
        "body",
        "locked_to_subscribers",
        "post_type",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "blog_post",
        "commenter",
        "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "blog_post",
        "user",
        "created_at",
    )


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = (
        "blog_post",
        "ip_address",
        "user",
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "blog_post",
        "owner",
        "text",
    )
