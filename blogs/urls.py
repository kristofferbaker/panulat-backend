from django.urls import path, include
from .views import *


blog_posts_urlpatterns = [
    path(
        "",
        ListBlogPostsAccountModeAPI.as_view(),
        name="list-blog-posts-account-mode",
    ),
    path(
        "create/",
        CreateBlogPostAPI.as_view(),
        name="create-blog-posts",
    ),
    # path(
    #     "",
    #     EditBlogPostAPI.as_view(),
    #     name="edit-blog-post",
    # ),
    # path(
    #     "",
    #     SoftDeleteBlogPostAPI.as_view(),
    #     name="soft-delete-blog-post",
    # ),
]


stats_urlpatterns = [
    path(
        "",
        StatsOverviewAPI.as_view(),
        name="stats-overview",
    ),
]

subscriptions_urlpatterns = [
    path(
        "",
        ListLatestPostsOfSubscribedToBlogsAPI.as_view(),
        name="list-latest-posts-of-subscribed-to-blogs",
    ),
]

explore_urlpatterns = [
    path(
        "global/",
        GlobalExploreAPI.as_view(),
        name="global-explore",
    ),
]

urlpatterns = [
    path("blog-posts/", include((blog_posts_urlpatterns, "blog-posts"))),
    path("stats/", include((stats_urlpatterns, "stats"))),
    path("subscriptions/", include((subscriptions_urlpatterns, "subscriptions"))),
    path("explore/", include((explore_urlpatterns, "explore"))),
]
