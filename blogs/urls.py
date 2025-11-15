from django.urls import path, include
from .views import GlobalExploreAPI


explore_urlpatterns = [
    path(
        "global/",
        GlobalExploreAPI.as_view(),
        name="global-explore",
    ),
]

urlpatterns = [
    path("explore/", include((explore_urlpatterns, "explore"))),
]
