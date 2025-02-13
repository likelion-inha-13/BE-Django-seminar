from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('create/',views.create_post), 
    path('get/<int:pk>/',views.get_post),
    path('all/',views.get_posts_all),
    path('update/<int:pk>/',views.update_post),
    path('delete/<int:pk>/',views.delete_post)
]