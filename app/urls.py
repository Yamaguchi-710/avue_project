from django.urls import path
from app import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("avue", views.Project_avue.as_view(), name="avue"),
    path("avue_easy", views.Project_avue_easy.as_view(), name="avue_easy"),
    path("private", views.Project_private.as_view(), name="private"),
]