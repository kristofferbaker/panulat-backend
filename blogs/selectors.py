from blogs.models import *
from accounts.models import CustomUser
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime
import pytz

from dateutil.relativedelta import relativedelta


def global_search(data):
    search_query = data["search_query"]

    matching_blogs = Blog.objects.filter(blog_name__icontains=search_query)

    return matching_blogs


def get_latest_blog_posts_of_subscribed_to_blogs(user):
    subscriptions = Subscription.objects.filter(email=user.email, is_active=True)
    latest_blog_posts = []

    # For each subscription:
    for subscription in subscriptions:
        # Get the latest blog post.
        blog = subscription.blog
        latest_blog_post = BlogPost.objects.filter(blog=blog).last()

        if latest_blog_post:
            latest_blog_posts.append(latest_blog_post)

    return latest_blog_posts


def get_stats(data, user):
    blog = Blog.objects.filter(pk=data["blog_pk"], blog_author=user).first()
    time_period_filter = data.get("time_period_filter")

    # Today filter arguments
    if time_period_filter == "T":
        end_date = timezone.datetime.today().date()
        start_date = timezone.datetime.today().date()

    # Yesterday filter arguments
    if time_period_filter == "Y":
        end_date = timezone.datetime.today().date() - timezone.timedelta(days=1)
        start_date = end_date

    # Last 7 days filter arguments
    if time_period_filter == "L7D":
        end_date = timezone.datetime.today().date()
        start_date = end_date - timezone.timedelta(days=7)

    # Last month filter arguments
    if time_period_filter == "LM":
        today = timezone.datetime.today().date()
        today_last_month = today - relativedelta(months=1)
        start_date = timezone.datetime(
            year=today_last_month.year, month=today_last_month.month, day=1
        ).date()
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

    # This year filter arguments
    if time_period_filter == "TY":
        end_date = timezone.datetime.today().date()
        start_date = timezone.datetime(year=end_date.year, month=1, day=1).date()

    # Last year filter arguments
    if time_period_filter == "LY":
        today = timezone.datetime.today().date()
        start_date = timezone.datetime(year=today.year - 1, month=1, day=1).date()
        end_date = timezone.datetime(
            year=today.year, month=1, day=1
        ).date() - relativedelta(days=1)

    # All time filter arguments
    if time_period_filter == "AT":
        end_date = timezone.datetime.today().date()
        start_date = blog.created_at.date()

    if blog == None:
        raise ValidationError("No such blog exists.")

    blog_posts = BlogPost.objects.filter(blog=blog)

    total_views = 0

    # For each blog post of the blog:
    for blog_post in blog_posts:
        if time_period_filter:
            # Get the total numbers of views for the blog post in the specified time range.
            views = View.objects.filter(
                blog_post=blog_post,
                created_at__range=(start_date, end_date + timezone.timedelta(days=1)),
            ).count()
        else:
            # Get the total numbers of views for the blog post.
            views = View.objects.filter(blog_post=blog_post).count()

        # Then add it to a sum.
        total_views = total_views + views

    if time_period_filter:
        total_subscribers = Subscription.objects.filter(
            blog=blog,
            is_active=True,
            created_at__range=(start_date, end_date + timezone.timedelta(days=1)),
        ).count()
    else:
        total_subscribers = Subscription.objects.filter(
            blog=blog, is_active=True
        ).count()

    return {"total_views": total_views, "total_subscribers": total_subscribers}


def get_blog_posts_account_mode(data, user):
    post_type = data.get("post_type")
    blog_posts = BlogPost.objects.filter(author=user, post_type=post_type)

    return blog_posts


def get_published_blog_posts_reading_mode(data):
    blog = data.get("blog")
    blog_posts = BlogPost.objects.filter(blog=blog, post_type="PU")

    return blog_posts


def get_blog_post_comments(data):
    blog_post = data.get("blog_post")
    comments = Comment.objects.filter(blog_post=blog_post, is_active=True)

    return comments


def get_subscription(data, user):
    return Subscription.objects.filter(blog=data.get("blog"), subscriber=user).first()
