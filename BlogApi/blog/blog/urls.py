"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from blog_api.views import home
from blog_api.views import about
from blog_api.views import sobre
from blog_api.views import detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name='home'),
     path('about', about , name='about'),
     path('sobre', sobre , name='sobre'),
     
     path('post/<int:id>/', detail, name='post_detail'),
     path('detail', detail , name='detail'),
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)