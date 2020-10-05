from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index_login"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
]
