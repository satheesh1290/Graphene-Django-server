# users/urls.py
from django.urls import path
# from .views import upload_avatar
from .views import FileUploadView, get_csrf_token
from .views import TestView

urlpatterns = [
    # path('upload-avatar/', upload_avatar, name='upload_avatar'),
    path('upload-avatar/', FileUploadView.as_view(), name='upload_avatar'),
    path('test/', TestView.as_view(), name='test_view'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]
