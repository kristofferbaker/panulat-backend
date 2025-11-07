from django.urls import path
from .views import TestAPI

urlpatterns = [path("accounts/create/", TestAPI.as_view())]


# http://127.0.0.1:8000/api/login/
# http://127.0.0.1:8000/api/logout/
# http://127.0.0.1:8000/api/password/reset
# http://127.0.0.1:8000/api/password/reset/confirm
# http://127.0.0.1:8000/api/registration/
