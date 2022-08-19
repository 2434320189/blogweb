from django import template
from blog.models import Category, Post,SideBar

register = template.Library()

@register.simple_tag
def get_category_list():
    return Category.objects.all()

@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()

@register.simple_tag
def get_new_post():
    # 获取最新文章
    return Post.objects.order_by('-pub_date')[:5]

@register.simple_tag
def get_hot_post():
    # 手动热门推荐
    return Post.objects.filter(is_hot=True)[:5]

@register.simple_tag
def get_hot_pv_post():
    # 自动热门推荐
    return Post.objects.order_by('-views')[:5]

@register.simple_tag
def get_archives():
    # 文章归档
    return Post.objects.dates('add_date', 'month', order='DESC')[:5]





