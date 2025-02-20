from django.urls import include, path
from . import views

urlpatterns = [
    path('signup', views.signup), # users/signup
    path('login', views.login), # users/login
]