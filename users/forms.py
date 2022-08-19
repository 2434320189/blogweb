from django import forms
from django.contrib.auth.models import User

from blog.admin import PostAdmin
from blog.models import Post
from .models import UserProfile

class CKEditorWidget(forms.Textarea):

    class Media:
        # css={'all': ('ckeditor5/cked.css'),}

        js= (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor5/build/ckeditor.js',
            'ckeditor5/build/translations/zh.js',
            'ckeditor5/config.js',
            # 'ckeditor5/sample/styles.css',

        )


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=25,widget=forms.TextInput(attrs={
        'class': 'input','placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input','placeholder': '密码'
    }))


    #判断用户名是否与密码相同
    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     if username == password:
    #         raise forms.ValidationError('密码不能与用户名一样！')
    #     return password

class RegisterForm(forms.ModelForm):

    username = forms.CharField(label='用户名', min_length=6, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名'}))
    email = forms.EmailField(label='邮箱地址', min_length=6, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '邮箱地址'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'}))

    class Meta:
        model = User
        fields = ('username', 'email','password')

    def clean_username(self):
        #取出用户名的值
        username = self.cleaned_data.get('username')

        #验证用户是否存在
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError("用户名已经存在！")
        return username

    def clean_email(self):
        #取出邮箱的值
        email = self.cleaned_data.get('email')

        #验证邮箱是否存在
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("邮箱已经存在！")
        return email

    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        if password != password1:
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password

    #判断用户名是否与密码相同
    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     if username == password:
    #         raise forms.ValidationError('密码不能与用户名一样！')
    #     return password

class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


class ModifyPwdForm(forms.Form):

    password = forms.CharField(label='输入新密码', min_length=6,widget=forms.PasswordInput(attrs={
        'class':'input', 'placeholder':'输入新密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'}))

    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        if password != password1:
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password


class UserForm(forms.ModelForm):
    """ User模型的表单，只允许修改email一个数据，用户名不允许修改 """
    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """ UserProfile的表单 """
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = ('name','nick_name','desc','phone','gexing', 'birthday',  'gender', 'address', 'image')

class ArticleForm(forms.ModelForm):
    """Form definition for Article."""
    title = forms.CharField(label="文章标题",
        widget=forms.TextInput(attrs={'class':'input'}))
    desc = forms.CharField(label="文章描述", widget=forms.Textarea(
        attrs={'class':'textarea', 'rows':4}
    ))
    content = forms.CharField(label="文章内容", widget=CKEditorWidget)



    class Meta:
        """Meta definition for Articleform."""

        model = Post
        exclude = ['author',]


