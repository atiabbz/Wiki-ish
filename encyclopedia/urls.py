from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.randomEntry, name="random"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
