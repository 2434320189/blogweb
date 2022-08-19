from django.urls import path
from . import views

app_name = 'users'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('login.html', views.login_view, name='login'),
    path('register.html',views.register_view,name='register'),
    path('active/<active_code>',views.active_user,name='active_user'),
    path('forget_pwd.html/', views.forget_pwd, name='forget_pwd'),
    path('forget_pwd_url.html/<active_code>', views.forget_pwd_url, name='forget_pwd_url'),
    path('user_profile.html/', views.user_profile, name='user_profile'),
    path('logout.html/', views.logout_view, name='logout'),
    path('editor_users.html',views.editor_users,name='editor_users'),
    path('password_change.html/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done.html/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('person_article.html/', views.person_article, name="person_article"),  # 查询当前登录用户已经发布的文章
    path('person_add_article.html/', views.person_add_article, name="person_add_article"),  # 添加文章
    path('article_delete/<int:id>', views.article_delete, name='delete_article'),   #删除文章
    path('person_article_delete.html/<int:post_id>', views.delete_page, name='delete_page'),
]