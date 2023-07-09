# pages/urls.py
from django.urls import path

from .views import RecordCreateView

urlpatterns = [
    # path('file-upload/', file_upload_view, name='file-upload'),
    path("create/", RecordCreateView.as_view(), name="create-record")
]
