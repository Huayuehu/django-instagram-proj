from annoying.decorators import ajax_request
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView # 用于操作form
from django.urls import reverse_lazy


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.models import Post, Like, InstaUser, Comment, UserConnection # views里面要找到model和template然后返回，所以也要import model
from Insta.forms import CustomUserCreationForm

# Create your views here.
class HelloWorld(TemplateView): # 我们自己创建的HelloWorld view，希望它继承TemplateView这个父类class，TemplateView是Django提供的已经写好了的class
    template_name = 'test.html' # 当用户请求InstaProj中指定的url之后，Django会自动get template_name，我们在这里指定template_name = "test.html"，Django就会自动去返回test.html这个页面

class PostsView(ListView):
    model = Post # 使用我们定义的model Post, 会把ListView自带的返回对象object_list返回给index.html以供使用
    template_name = 'index.html' # render index.html这个页面

    def get_queryset(self): # ListView中default的get_queryset()是会返回所有的Post，但在这里重写这个函数，进行filter，只返回当前following user的posts
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('followed'):
            following.add(conn.followed)
        return Post.objects.filter(author__in=following)


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

class UserDetailView(DetailView):
    model = InstaUser
    template_name = "user_detail.html"

# CreateView会返回一个form给post_create.html使用; 
# LoginRequiredMixin表示要访问create post这个view必须先通过LoginRequiredMixin验证，i.e.处于log in的状态，如果没有login就跳转到login_url
class PostCreateView(LoginRequiredMixin, CreateView): 
    model = Post
    template_name = "post_create.html"
    fields = '__all__'  # 当create a model时，需要提供model定义class时提到的所有的field
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title'] # 只允许用户update title这个field
    template_name = 'post_update.html'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts') # 当删除这个操作成功了之后，返回到success_url这个url； 为什么不用reverse，因为不能边删除边跳转页面，所以用reverse_lazy

class SignUp(CreateView):
    form_class = CustomUserCreationForm # 用django auth自带的UserCreationForm或者自定义的CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


@ajax_request # 这个函数是用于相应ajax request，不需要依附于任何class
def addLike(request):
    post_pk = request.POST.get('post_pk') # 先拿到被like了的post的pk
    post = Post.objects.get(pk=post_pk) # 由pk找到Post中那个object
    try:
        like = Like(post=post, user=request.user) # 用当前的post和user创建一个like的对象
        like.save() # 把刚刚创建的对象存入数据库中；如果这个对象已经存在，跳到下面的exception
        result = 1
    except Exception as e: # 已经点过的like再被点，说明要取消这个like，所以从数据库中删除
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }