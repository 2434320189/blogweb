from django.contrib import admin
from django.contrib.auth.models import User     # 首先引入User
from django.contrib.auth.admin import UserAdmin     # 我们看到的这个用户选项就是官方默认通过UserAdmin这个类注册到后台的，那么我们也引入进来，后边继承这个类
from .models import UserProfile     # 再引入我们定义的模型
from .models import EmailVerifyRecord

admin.site.unregister(User)     # 必须先通过unregister将User取消注册

# 定义关联对象的样式，StackedInline为纵向排列每一行，TabularInline为并排排列
class UserProfileInline(admin.StackedInline):
    model = UserProfile   # 关联的模型

# 关联字段在User之内编辑，关联进来
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for EamilVerifyRecord'''
    list_display = ('code',)


# Register your models here.
# 重新注册User
admin.site.register(User, UserProfileAdmin)