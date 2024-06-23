    
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.get_users, name='get_all_users'),
    path('users/<str:nick>/', views.get_nick, name='get_nick_name'),
    path('data/',views.get_all),
    path('post/',views.post_data)
    
]
