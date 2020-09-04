"""InstaProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views 如果我们在views中定义的是class based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf 可以导入app level的url configuration
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project level的url
from django.contrib import admin
from django.urls import include, path

from Insta.views import SignUp

urlpatterns = [
    path('admin/', admin.site.urls), # 默认地以管理员身份登录
    path('', include('Insta.urls')), # 如果你所传入的路径是以insta开头的，就是用Insta.urls这个app level的url config
    path('auth/', include('django.contrib.auth.urls')), # 以auth开头的路径，交给django自带的auth app来处理
    path('auth/signup/', SignUp.as_view(), name='signup'),
]
