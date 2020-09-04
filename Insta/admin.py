from django.contrib import admin

from Insta.models import InstaUser, Like, Post, UserConnection

# Register your models here.
admin.site.register(Post) # 在admin的model中注册一个post
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(UserConnection)