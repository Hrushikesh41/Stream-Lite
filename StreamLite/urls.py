"""
URL configuration for StreamLite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup, name='signup'),
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('upload/', upload_video, name='upload_video'),
    path('video/<int:id>/', video_detail, name='video_detail'),
    path('profile/', user_profile, name='user_profile'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    path('video/<int:video_id>/like/', like_video, name='like_video')
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)