from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#用户模型
class UserProfile(models.Model):
    #设置一个选项，用于显示在页面上
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
    )
    owner = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')
    name = models.CharField("姓名",max_length=23,blank=True,default='暂未填写姓名')
    nick_name = models.CharField("昵称",max_length=23,blank=True,default='暂未设置昵称')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField('地址', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.jpg', max_length=100, verbose_name='用户头像')
    desc = models.TextField('个人简介',max_length=200,blank=True,default='暂未设置个人简介')
    gexing = models.CharField('个性签名',max_length=100,blank=True,default='暂未设置个人签名')
    phone = models.CharField('手机号', unique=True, max_length=11,default='暂未设置')
    # add_date = models.DateField('注册日期', auto_now_add=True,null=True)

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username

#邮箱验证模型
class EmailVerifyRecord(models.Model):
    # 设置一个选项，用于显示在页面上
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


