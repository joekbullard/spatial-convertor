# pages/urls.py
from django.urls import path

from .views import HomeView, file_upload_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('file-upload/', file_upload_view, name='file-upload'),
]
