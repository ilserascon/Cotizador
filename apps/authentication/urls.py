# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
      # Authentication
    path('login/', views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path("create-user", views.create_user, name="create-user"),
    path("edit-user/<int:id>", views.edit_user, name="edit-user"),
    path("get-users", views.get_users, name="get-users"),
    path("delete-user/<int:id>", views.delete_user, name="delete-user")

]

