## Django Web Application

### Build a Development Environment

- Django
- Python

**Install Python Virtual Environment**

I use python virtualenv.

Under the file DjangoDev, use `virtualenv -p python3 venv` to create a independent Python virtual environment. That environment will be place to ./venv path

To activate the enviroment, type `source venv/bin/active`; To leave: `deactivate` 

For pipenv:

pip3 install pipenv

Inside the project folder: 

	- `pipenv install Django`
	- `pipenv shell` to start the virtual env
	- `exit` for exit virtual env

**Install Django**

Inside the virtual environment, use `pip3 install django` to install Django.

Then, type `django-admin startproject InstaProj . ` to start a project with name InstaProj, "." means the file will be inside current file. 

**Run Server**

`cd DjangoDev` change directory to which *manage.py* is located. 

Type `python3 manage.py runserver` to run local web server. Go to http://127.0.0.1:8000/ to verify the server is up and running.

**All files**

***manager.py*** to excute all kinds of django commands

***setting.py*** is the project level settings

***urls.py*** is url routing management

***wsgi.py*** is web server gateway interface, to describe how server communicate with application

---

### 一

* Create a project
* Create a app to power up static page
* MVC Introduction
* Template Settings
* View Settings
* URLConf Settings

**Inside the project, we create an app**

`python manage.py startapp Insta` 

**project vs app**

one project has lots of app for different part

**Inside *Insta* app: **

*app.py*: 与project中的*setting.py*相对应，是app level的configuration

*migration*: 记录django model和database之间的变化，使得每次DB migration的时候都能保持sync

*models.py*: 在里面定义database的models，django可以把它转成DB tables，每一个table对应一个model

*test.py*: app-specifi tests(??????)

*views.py*: to handle request/response

**Connect project and app**

In spite of the creation of insta app, but the project doeesn't know the existence of this app. Therefore, we need to claim each app inside setting.py

### MVC  Design pattern

Relation: MODEL updates VIEW sees USER uses CONTROLLER(附加在VIEW页面上的button) manipulates MODEL

**MVC in Django - Model / View / Template**

MODEL - MODEL(in MVC)

VIEW - CONTROLLER(in MVC)

TEMPLATE - VIEW(in MVC)

Model: Database model

View: 决定在一个页面上能显示什么内容，控制着如何响应request以及如何返回response。Django有class-based views，我们可以继承Django已有的各种views类型

Template: to store different html page

**Try with static hello world page**

当有人访问这个URL时，这个URL能和一个view连接起来，然后从template中把能显示hello world的页面调出来发送回去。

1. 创建一个templates folder，里面装test.html

2. 在setting中连接templates，在TEMPLATES中指定刚刚创建的templates folder的路径

3. Insta-views.py中要把url跟.html连接起来，当有人请求这个url时把对应的html render出去

   1. Views里面的概念：

      Class-Based Views: 根据不同的场景需求，Django提供的各种View类型，我们可以继承相思的类型来减少代码量利于重复开发

**Setting URL Confs**

1. Modify Project level urls.py to link apps

   e.g.

   ```
   urlpatterns = {
   	path('insta/', include('Insta.urls')).
   }
   ```

2. Add app level urls.py to handle URL configuration inside app

---

### 二

* Define Django models
* Sync database
* Update Admin
* Template & View & URLConf Settings

**Django MTV pattern**

![IMG_F23C90F13AC0-1](/Users/insane/Downloads/IMG_F23C90F13AC0-1.jpeg)

**Django models**

Django framework can map django.db.models.Models to database tables

Django can support four database:

* MySQL
* PostgreSQL
* Oracel
* SQLite (default)

在model中创建class Post

**Sync Database**

每次在model中新加了某个model的class，就会在migrations里创建files表示从上次migrate到现在，需要在数据库里做哪些变化，使得数据库中能update到最新。

所以当我在model中创建了class Post之后要通过下面两个语句让这个表在数据库中被生成：

`python manage.py makemigrations`: create a migration file for every installed apps in project settings.py

`python manage.py migrate`: excute the defined content inside this migration执行上一步生成的文件，使得database中产生新的table

**Update Admin**

在Django自带的针对database提供的一个admin interface中更新，默认需要super user登录

`python manage.py createsuperuser` to create super user and logging in 127.0.0.1/8000/admin as the created super user

**CMS(Content Management System)**

管理网站的内容

1. 创建super user：`python manage.py createsuperuser`
2. 登录网站上添加数据

---

### 三

* Realize master/detail structure
* Deeper Class-Based View
* Django forms
* CRUD

**Django Forms**

FormView, CreateView, UpdateView, DeleteView等是Django提供的用于处理表格的class，以实现form常用的基本操作

---

### 四

**Authentication**

Django提供了一个Auth System

1. 自带有login和logout的功能



**Customize user model**

Django自带的user model比较死板，里面的field有局限性，所以可以customize你自己的user model:

1. 在model中新建一个InstaUser继承Django自带的AbstractUser，同时添加profile_pic这个新的field
2. 然后在setting.py中指明AUTH_USER_MODEL = ‘Insta.InstaUser"，那样auth就不会用django默认的user model了
3. 考虑在哪些地方用到了user model，要去更新为customized user model：
   - admin.py: 在admin的网站中心注册一个InstaUser的model
   - 在注册时要用输入的信息创建一个user的对象，之前是用旧的model，现在更新成自定义的：
     1. 在Insta这个app中新建一个forms.py来装我们自定义的forms，在里面创建一个*CustomUserCreationForm*继承Django自带的UserCreationForm
     2. 在views.py里的SignUp class中更新form_class为*CustomUserCreationForm*

---

### 五 美化前端

- 用Django Template Language
  1. 创建base.html和header.html作为所有页面通用的模板
  2. 在所有页面中导入

```django
{% extends "base.html" %}

{% block content %}

[body]

{% endblock content %}
```



- 对每个图片点爱心的时候，想要likes的数量出现变化，并且爱心的样式出现变化，这种局部的变化需要用户自定义template language：
  1. 根据Django的规定，自定的template language要放在app folder下面的一个templatetags folder中。在里面定义一个函数has_user_liked_post()来根据当前登录的用户是否跟某个post有like关系来返回不同形式的爱心==>成功依据用户来显示爱心样式
  2. 在static folder下的js folder中，创建一个index.js，用于处理，当爱心被click了，likes数量和爱心样式发生变化。里面用到了ajax。

---

### 六 Profile和follow等社交关系

