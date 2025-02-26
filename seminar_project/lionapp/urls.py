from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('members/create/', views.create_member),
    path('members/get/<int:pk>/', views.get_members),
    path('members/change_password/<int:pk>/', views.change_password),
    path('members/click_hearts/<int:pk>/', views.click_hearts),
    path('members/leader/<int:pk>/', views.leader),
    path('members/leader/<int:pk>/', views.leader_v2),
    path('members/get_all/', views.get_all_members)
]