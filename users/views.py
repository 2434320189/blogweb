from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, DeleteView,UpdateView
from django.utils.translation import gettext_lazy as _
from blog.models import Category, Tag, Post
# from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ArticleForm
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.models import User
from .models import EmailVerifyRecord, UserProfile # 引入用户模型字段
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm
# Create your views here.


#用户验证
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   # 加密明文密码
                return user
        except Exception as e:
            return None

def login_view(request):
    #判断收到的请求是否为POST
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():     #如果检验全部通过，则获取接收到的信息
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            #如果登录信息正确
            if user is not None:
                login(request, user)
                # 登陆成功跳转到指定页面
                # return HttpResponse('登陆成功')
                return redirect('/blog/index.html')
            else:
                # 验证不通过提示！
                return HttpResponse("账号或者密码错误！")
    context = {'form': form}
    return render(request, 'users/login.html', context)

def register_view(request):
    #判断是否为post请求，如果是get请求则返回表单，如果是post则将请求传给forms.py处理并将
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        #如果请求结果不为空，is_valid()函数的作用是将表单的提交值进行校验，检验值是否符合预设的类型，如果正确返回true，否则返回false
        if form.is_valid():
            #先将用户信息暂存起来给一个新的new_user对象
            new_user = form.save(commit=False)

            #从暂存的值中提取密码，然后将密码转化为哈希值然后在放回暂存数据中，cleaned_data函数的作用是将表单中name为**的值取出，set_password的作用为将密码加密
            new_user.set_password(form.cleaned_data['password'])

            #将转化为哈希值的密码和其他信息存进数据库
            new_user.save()
            #发送注册邮件
            send_register_email(form.cleaned_data.get('email'),'register')
            #跳转到登录页面
            return redirect('users:login')

    context = {'form': form}
    return render(request, 'users/register.html', context)

def active_user(request, active_code):
    """查询验证码"""
    print(active_code)
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    print(all_records)
    if all_records:
        for record in all_records:
            email = record.email
            print(email)
            user = User.objects.get(email=email)
            print(user)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('链接有误！')
    return redirect('users:login')

def forget_pwd(request):
    """ 找回密码 """
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            #检查邮箱是否存在
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('邮件已经发送请查收！')
            else:
                return HttpResponse('邮箱还未注册，请前往注册！')

    return render(request, 'users/forget_pwd.html', {'form': form})

def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)

            user.password = make_password(form.cleaned_data.get('password'))

            user.save()
            return HttpResponse('修改成功')

    return render(request, 'users/reset_pwd.html', {'form': form})

@login_required(login_url='users:login')   # 设置登录后才能访问，如果没有登陆，就跳转到登录界面
def user_profile(request):
    user=User.objects.get(username=request.user)
    return render(request,'users/user_profile.html',{'user': user})

def logout_view(request):
    logout(request)
    return redirect('blog:index')

# 本视图登录后才能访问，所以检测登录的装饰器一定要加

@login_required(login_url='users:login')
def editor_users(request):
    """ 编辑用户信息 """
    return render(request, 'users/editor_users.html')

@login_required(login_url='users:login')   # 登录之后允许访问
def editor_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值填进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()

                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'users/editor_users.html', locals())

def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category_list.html', context)

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'users/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required(login_url='login')
def person_article(request):
    # 查询当前用户已经发布的文章
    article_list = Post.objects.filter(owner=request.user).order_by('pub_date')
    return render(request, 'users/person_article.html', locals())


@login_required(login_url='login')
def person_add_article(request):
    # 添加文章
    user = User.objects.get(id=request.user.id)
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    if request.method != 'POST':
        form = ArticleForm()
    else:
        # 创建表单，并获取表单中的数据
        form = ArticleForm(request.POST)
        form.owner=user.username
        print(form,'--------------------------')
        if form.is_valid():
            # 暂存数据，并返回一个类s字典数据
            new_article = form.save(commit=False)
            # 将作者信息加入到这个类字典
            # new_article.owner = request.POST.get('owner')
            new_article.content = request.POST.get('content')
            new_article.save()  # 保存
            # 获取多对多的tags文章标签，getlist()方法获取多选数据
            tags = request.POST.getlist('tags')
            # 获取到刚才创建的这篇文章
            b = Post.objects.get(id=new_article.id)
            # 使用set()方法将tags关联到文章
            # b.tags.set(tags)
            form.save_m2m()  # 保存多对多数据
            return redirect('users:person_article')
    return render(request, 'users/person_add_article.html', locals())

def delete_page(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'users/person_article_delete.html',context)

def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = Post.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("users:person_article")









