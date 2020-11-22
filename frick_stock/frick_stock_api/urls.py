from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path("hello/", HelloView.as_view()),
    path("follows/", FollowsView.as_view()),
    path("user/", ClientDetailView.as_view())
]