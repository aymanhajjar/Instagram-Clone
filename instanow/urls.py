"""instanow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from users import views as userviews
from home import views as homeviews
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeviews.homepage, name ="home"),
    path('register/', userviews.register, name = "register"),
    path("logout", userviews.userlogout, name="logout"),
    path('login/', userviews.userlogin, name = "login"),
    path('explore/', homeviews.explore, name = "explore"),
    path('profile/<str:username>', homeviews.userprofile, name = "profile"),
    path('profile/<str:username>/settings/', homeviews.editprofile, name = "editprofile"),
    path('p/<int:postid>', homeviews.postdetails, name = "postdetails"),
    path('profile/<str:username>/tagged', homeviews.taggedposts, name="tagged"),
    path('profile/<str:username>/saved', homeviews.savedposts, name="saved"),
    path('p/<int:postid>/likers', homeviews.postlikers, name="likers"),
    path('p/<int:postid>/like', homeviews.likepost, name="like"),
    path('p/<int:postid>/addcomment', homeviews.addcomment, name="addcomment"),
    path('p/<int:postid>/unlike', homeviews.unlikepost, name="unlike"),
    path('p/<int:postid>/save', homeviews.savepost, name="save"),
    path('p/<int:postid>/unsave', homeviews.unsavepost, name="unsave"),
    path('profile/<str:targetuser>/follow', homeviews.follow, name="follow"),
    path('profile/<str:targetuser>/unfollow', homeviews.unfollow, name="unfollow"),
    path('search/<str:query>', homeviews.search, name="search"),
    path('newpost/', homeviews.newpost, name="create"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)