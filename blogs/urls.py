from django.urls import path, include
from .views import *


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
    path("stats/", include((stats_urlpatterns, "stats"))),
    path("subscriptions/", include((subscriptions_urlpatterns, "subscriptions"))),
    path("explore/", include((explore_urlpatterns, "explore"))),
]
