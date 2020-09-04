"""InstaProj URL Configuration

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
# app level的url
# 在这个app level url中，我们处理的是Class-based views的url处理方式
from django.contrib import admin
from django.urls import include, path

from Insta.views import (HelloWorld, PostDetailView, PostsView, 
                        PostCreateView, PostUpdateView, PostDeleteView, 
                        addLike, addComment, UserDetailView, toggleFollow)  # 从Insta.views这个文件中import HelloWorld这个view

urlpatterns = [
    path('hellowrold', HelloWorld.as_view(), name='helloworld'), # 如果传入路径是空，默认访问HelloWorld的as_view()这个函数（这个函数是在TemplateViews里定义的）
    path('', PostsView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), # 将post/后面的int当做去数据库里查找的primary key -> 用于查找
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('like', addLike, name='addLike'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('togglefollow', toggleFollow, name='toggleFollow'),
]
