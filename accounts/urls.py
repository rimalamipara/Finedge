from django.urls import path as url
from . import views

app_name = "accounts"

urlpatterns = [
    url("register/", views.register, name = "signup"),
    url("login/", views.sign_in, name = "signin"),
    url("logout/", views.logout_view, name = "logout"),
]
