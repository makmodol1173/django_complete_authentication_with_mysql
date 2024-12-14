from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.logout, name='logout'),
    path('upload-picture/', views.upload_picture, name='upload_picture'),
]
