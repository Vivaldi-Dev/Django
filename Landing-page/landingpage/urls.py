from django.urls import path
from . import views

urlpatterns = [
    path('list', views.BlogView.as_view(), name='get_all'), 
    path('get',views.SnippetList.as_view())  ,
]
