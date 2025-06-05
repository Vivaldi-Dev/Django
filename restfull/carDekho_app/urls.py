f
rom django.urls import path
from . import views
urlpatterns = [
    path("list", views.car_list, name="car list"),
    path("list/<int:pk>", views.car_detail_view, name="car detail"),
    path("showroom", views.Showroom_View.as_view(), name="showroom"),
    path("showroom/<int:pk>", views.Showroom_detail.as_view(), name="Showroom_detail"),
    path("users/",views.showUser.as_view(),name="user-list"),
    path("carobject", views.showobject.as_view(),name="object"),
    path("review",  views.SnippetList.as_view(),name="review"),
    path('review/<int:pk>',views.SnippetDetail.as_view(),name="reviewlist"),
    path('reviewput/<int:pk>',views.Reviewdetail.as_view(),name="review put")
]
