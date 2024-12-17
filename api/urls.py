from django.urls import path, include
from . import views

urlpatterns = [
    path('upload_data', views.DataUpload.as_view(), name='upload_data'),
    ]
