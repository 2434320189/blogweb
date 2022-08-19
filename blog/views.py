from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.shortcuts import render, get_object_or_404
from blog.models import Category, Post, Tag


# Create your views here.



def index(request):
    category_list = Category.objects.all()  # 查询到所有的分类
    post_list = Post.objects.all()  # 查询到所有的文章
    paginator = Paginator(post_list, 6)  # 第二个参数2代表每页显示几个box
    page_number = request.GET.get('page')   #page关键字指的是url连接中的page字段
    page_obj = paginator.get_page(page_number)

    context = {'category_list': category_list, 'post_list': post_list,'page_obj': page_obj}  # 上下文数据

    return render(request, 'blog/index.html',context)

def category_list(request, category_id):
    #文章类型列表页
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    paginator = Paginator(posts, 6)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj }
    return render(request, 'blog/category_list.html', context)

def post_list(request,post_id):
    #文章详情页
    post=get_object_or_404(Post,id=post_id)

    #阅读量+1
    post.increase_views()

    #按照id排序
    # prev_post= Post.objects.filter(id__lt=post_id).last()
    # next_post= Post.objects.filter(id__lt=post_id).first()

    #按照发布时间排序
    prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    next_post = Post.objects.filter(add_date__gt=post.add_date).first()

    # print(prev_post,next_post)
    context={'post':post,'prev_post':prev_post,'next_post':next_post}
    return render(request,'blog/detail.html',context)

def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')  # 获取表单中输入的值

    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))

    paginator = Paginator(post_list, 6)  # 第二个参数2代表每页显示几个box
    page_number = request.GET.get('page')   #page关键字指的是url连接中的page字段
    page_obj = paginator.get_page(page_number)

    context = {'post_list': post_list,'page_obj': page_obj}
    return render(request, 'blog/index.html', context )

def archives(request,year,month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    context = {'post_list': post_list, 'year': year, 'month': month}
    return render(request, 'blog/sidebar/archives_list.html', context)




