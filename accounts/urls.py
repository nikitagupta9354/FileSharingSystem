from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name= 'logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('clientUserDashboard/', views.clientUserDashboard, name='clientUserDashboard'),
    path('opsUserDashboard/', views.opsUserDashboard, name='opsUserDashboard'),
]
