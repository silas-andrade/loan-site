from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginPage, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
