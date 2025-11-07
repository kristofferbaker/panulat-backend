from django.urls import path
from .views import TestAPI

urlpatterns = [path("blogs/create/", TestAPI.as_view())]
