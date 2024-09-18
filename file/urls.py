from django.urls import path
from . import views
urlpatterns = [
    path('upload/', views.uploadFile, name='uploadFile'),
    path('download/', views.downloadFile, name='downloadFile'),
]
