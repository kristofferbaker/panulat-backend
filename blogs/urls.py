from django.urls import path, include
from .views import *

profile_urlpatterns = [
    path(
        "edit-profile-banner/",
        EditProfileBannerAPI.as_view(),
        name="edit-profile-banner",
    ),
    path(
        "edit-profile-picture/",
        EditProfilePictureAPI.as_view(),
        name="edit-profile-picture",
    ),
    path(
        "reads/",
        ReadsTabAPI.as_view(),
        name="get-reads",
    ),
    path(
        "likes/",
        LikesTabAPI.as_view(),
        name="get-likes",
    ),
    path(
        "comments/",
        CommentsTabAPI.as_view(),
        name="get-comments",
    ),
    path(
        "posts/",
        PostsTabAPI.as_view(),
        name="get-posts",
    ),
    path(
        "",
        GetProfileAPI.as_view(),
        name="get-profile",
    ),
]


comments_urlpatterns = [
    path(
        "like-or-remove-like-comment/",
        LikeOrRemoveLikeCommentAPI.as_view(),
        name="like-or-remove-like-comment",
    ),
    path(
        "update/<pk>/",
        UpdateBlogPostCommentAPI.as_view(),
        name="update-blog-post-comment",
    ),
    path(
        "delete/<pk>/",
        DeleteBlogPostCommentAPI.as_view(),
        name="delete-blog-post-comment",
    ),
    path(
        "",
        ListBlogPostCommentsAPI.as_view(),
        name="list-blog-post-comments",
    ),
    path(
        "create/",
        CreateBlogPostCommentAPI.as_view(),
        name="create-blog-post-comment",
    ),
    path(
        "<pk>/",
        GetBlogPostCommentAPI.as_view(),
        name="get-blog-post-comment",
    ),
]


reading_mode_urlpatterns = [
    path(
        "get-latest-ten-blog-posts-of-blog/<pk>/",
        GetLatestTenBlogPostsofBlogAPI.as_view(),
        name="get-latest-ten-blog-posts-of-blog",
    ),
    path(
        "filter-blog-posts/",
        FilterBlogPostsofBlogAPI.as_view(),
        name="filter-blog-posts-of-blog",
    ),
    path(
        "like-or-remove-like-post/",
        LikeOrRemoveLikeBlogPostAPI.as_view(),
        name="like-or-remove-like-blog-post",
    ),
    path(
        "",
        ListPublishedBlogPostsReadingModeAPI.as_view(),
        name="list-blog-posts-reading-mode",
    ),
    path(
        "<pk>/",
        BlogPostDetailReadingModeAPI.as_view(),
        name="blog-post-detail-reading-mode",
    ),
]


account_mode_urlpatterns = [
    path(
        "list-latest-posts-of-subscribed-to-blogs/",
        ListLatestPostsOfSubscribedToBlogsAPI.as_view(),
        name="list-latest-posts-of-subscribed-to-blogs",
    ),
    path(
        "get-blogs-of-user/",
        GetBlogsOfUserAPI.as_view(),
        name="get-blogs-of-user",
    ),
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
    path(
        "update/<pk>/",
        UpdateBlogPostAPI.as_view(),
        name="update-blog-post",
    ),
    path(
        "delete/<pk>/",
        SoftDeleteBlogPostAPI.as_view(),
        name="soft-delete-blog-post",
    ),
    path(
        "<pk>/",
        BlogPostDetailAPI.as_view(),
        name="blog-post-detail",
    ),
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
        "subscribe/",
        SubscribeToBlogAPI.as_view(),
        name="subscribe-to-blog",
    ),
    path(
        "unsubscribe/<pk>/",
        UnsubscribeToBlogAPI.as_view(),
        name="unsubscribe-to-blog",
    ),
    path(
        "get-subscription/",
        GetSubscriptionAPI.as_view(),
        name="get-subscription",
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
    path(
        "profile/",
        include((profile_urlpatterns, "profile")),
    ),
    path(
        "comments/",
        include((comments_urlpatterns, "comments")),
    ),
    path(
        "reading-mode/",
        include((reading_mode_urlpatterns, "reading-mode")),
    ),
    path(
        "account-mode/",
        include((account_mode_urlpatterns, "account-mode")),
    ),
    path("stats/", include((stats_urlpatterns, "stats"))),
    path("subscriptions/", include((subscriptions_urlpatterns, "subscriptions"))),
    path("explore/", include((explore_urlpatterns, "explore"))),
]
