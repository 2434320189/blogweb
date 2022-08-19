from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('index.html', views.index, name='index'),
    path('category_list.html/<int:category_id>/', views.category_list, name='category_list'),
    path('detail.html/<int:post_id>/', views.post_list, name='post_detail'),
    path('search.html/', views.search, name='search'),
    path('archives.html/<int:year>/<int:month>/', views.archives, name='archives')
]
