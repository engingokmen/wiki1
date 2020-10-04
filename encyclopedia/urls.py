from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_detail, name="entry_detail"),
    path("search-result/<str:query>", views.search_result, name="search_result"),
    path("create-new-page", views.create_new_page, name="create_new_page"),
    path("wiki/<str:title>/edit-page/", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page"),
]
