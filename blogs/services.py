from django.db import transaction
from blogs.models import *
from accounts.models import UserProfile
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
    post_type = data.get("post_type")

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
        post_type=post_type,
    )

    return blog_post


@transaction.atomic
def update_blog_post(data, pk, user):
    blog_post = BlogPost.objects.filter(pk=pk).first()

    # Check if the editor is the author of the post:
    if blog_post.author != user:
        raise ValidationError("Not allowed.")

    # Get the updated data.
    blog = data.get("blog")
    opening_graphic = data.get("opening_graphic", None)
    title = data.get("title")
    subtitle = data.get("subtitle")
    body = data.get("body")
    locked_to_subscribers = data.get("locked_to_subscribers")
    post_type = data.get("post_type")

    # Update the blog post with the data.
    blog_post.blog = blog

    if opening_graphic:
        blog_post.opening_graphic = opening_graphic

    blog_post.title = title
    blog_post.subtitle = subtitle
    blog_post.body = body
    blog_post.locked_to_subscribers = locked_to_subscribers
    blog_post.post_type = post_type
    blog_post.save()

    return blog_post


@transaction.atomic
def like_or_remove_like_blog_post(data, user):
    like = Like.objects.filter(blog_post=data.get("blog_post"), user=user).first()

    # If user has already liked the blog post and cliked like again:
    if like:
        # Remove their like.
        like.delete()
    # If user has not yet liked the blog post:
    else:
        # Create a like for the blog post.
        Like.objects.create(blog_post=data.get("blog_post"), user=user)


@transaction.atomic
def create_blog_post_comment(data, user):
    blog_post = data.get("blog_post")
    commenter = user
    body = data.get("body")

    comment = Comment.objects.create(
        blog_post=blog_post,
        commenter=commenter,
        body=body,
    )

    return comment


def update_blog_post_comment(data, pk, user):
    comment = Comment.objects.get(pk=pk)
    body = data.get("body")

    if comment.commenter != user:
        raise ValidationError("Not allowed.")

    comment.body = body
    comment.save()

    return comment


@transaction.atomic
def like_or_remove_like_comment(data, user):
    # If user has already liked the comment and cliked like again:
    comment_like = CommentLike.objects.filter(
        comment=data.get("comment"), user=user
    ).first()
    if comment_like:
        # Remove their like.
        comment_like.delete()
    # If user has not yet liked the comment:
    else:
        # Create a like for the comment.
        CommentLike.objects.create(comment=data.get("comment"), user=user)


@transaction.atomic
def subscribe_to_blog(data, user):
    blog = data.get("blog")
    subscription = Subscription.objects.filter(blog=blog, subscriber=user).first()

    # If user has not yet subscribed to the blog
    if subscription == None:
        # create the subscription.
        Subscription.objects.create(email=user.email, subscriber=user, blog=blog)
    # If user has subscribed but then unsubscribed
    elif subscription.is_active == False:
        # reactivate subscription.
        subscription.is_active = True
        subscription.save()


def edit_profile_picture(data, user):
    user_profile = UserProfile.objects.filter(user=user).first()
    new_profile_picture = data.get("profile_picture")

    # Update user profile with the new picture.
    user_profile.profile_picture = new_profile_picture
    user_profile.save()

    return user_profile


def edit_profile_banner(data, user):
    user_profile = UserProfile.objects.filter(user=user).first()
    new_profile_banner = data.get("profile_banner")

    # Update user profile with the new banner.
    user_profile.profile_banner = new_profile_banner
    user_profile.save()

    return user_profile
