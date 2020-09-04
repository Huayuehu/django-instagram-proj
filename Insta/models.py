from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField # Django中常见的第三方的显示图片的库
from django.urls import reverse # 用于处理url常见的函数

# # Create your models here.
# # Define a model for picture post

class InstaUser(AbstractUser): # 自定义的user model继承了django自带的AbstractUser的属性，同时可以自己添加customized fields
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles', # 指定图片上传后的存储地址
        format='JPEG',
        options={'quality':100},
        blank=True, # 图片可以是空或者不存在
        null=True,
    )
    def get_connections(self): # 获得所有我在follow的人
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self): # 获得所有follow我的人
        followers = UserConnection.objects.filter(followed=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(followed=self) # 先拿到所有在follow我的人
        return followers.filter(creator=user).exists() # 在那里面查找，在follow我的人里面是否有当前的user

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set") # 本人去follow别人，user.friendship_creator_set返回的是我正在follow的所有人
    followed = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set") # 返回follow我的所有人

    def __str__(self):
        return self.creator.username + ' follows ' + self.followed.username


class Post(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, # foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='my_posts', # we can use author.my_posts to get all posts belong to this user
    )
    title = models.TextField(blank=True, null=True) # title的类型是Django自带的TextField，括号中的参数表示title为空或者完全没有title也可以post出去
    image = ProcessedImageField(
        upload_to='static/images/posts', # 指定图片上传后的存储地址
        format='JPEG',
        options={'quality':100},
        blank=True, # 图片可以是空或者不存在
        null=True,
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self): # 当有人保存了一个post对象，会自动跳转到get_absolute_url这个函数里返回的地方
        return reverse('post_detail', args=[str(self.id)]) # reverse用于找到某个页面对应的url，在这里是跳转到刚刚保存的那个post对应的detail信息的网页，detail这个网页需要传id这个参数，所有后面传进去

    def get_like_count(self):
        return self.likes.count() # 返回所有作用于这个post.likes的数量

    def get_comment_count(self):
        return self.comments.count()

class Like(models.Model): # Like是一个关系型model，连接了Post和InstaUser这两个model
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, # 定义了这样一个操作：如果post被删除，那整个like关系应该被删除
        related_name='likes')  # 用某个post.likes可以返回所有给这篇post点过赞的users

    user = models.ForeignKey(
        InstaUser, 
        on_delete=models.CASCADE, # 定义了这样一个操作：如果post被删除，那整个like关系应该被删除
        related_name='likes')  # 用某个user.likes可以返回所有给这个user点过赞的所有posts

    class Meta:
        unique_together = ("post", "user") # 一个user只能给一个特定的post点一次赞

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',)

    user = models.ForeignKey(
        InstaUser, 
        on_delete=models.CASCADE, 
        related_name='comments')

    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment