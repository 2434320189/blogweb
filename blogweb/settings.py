"""
Django settings for blogweb project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@1$_wp4copbfo$e(31@g#*8+i66oim9g)a$zm5a%20ugv8*o^l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
AUTHENTICATION_BACKENDS = (
    'users.views.MyBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',         #管理员站点
    'django.contrib.auth',          #认证授权系统
    'django.contrib.contenttypes',  #内容类型框架
    'django.contrib.sessions',      #会话框架
    'django.contrib.messages',      #消息框架
    'django.contrib.staticfiles',   #用于管理静态文件
    'blog.apps.BlogConfig',         #blog应用
    'users.apps.UsersConfig',       #users应用(用户中心)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogweb',
        'USER': 'blogweb',
        'PASSWORD': '243432',
        'HOST': '116.205.189.31',
        'PORT': '9010',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia\Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 定义静态文件的存放位置目录
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # '/var/www/static/',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = 'smtp.163.com'   # 用于发送电子邮件的主机。
EMAIL_HOST_USER = "19983149869@163.com"    # 自己的邮箱地址
# EMAIL_HOST_PASSWORD = "gzdycxwogyhqebdd"       # qq smtp 授权码
EMAIL_HOST_PASSWORD = "QZFHLRAZPGBFTGKM"       # 163 smtp 授权码
EMAIL_PORT = 465                     # 用于中定义的SMTP服务器的端口
EMAIL_USE_SSL = True             # 是否使用隐式的安全连接
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#将发送的邮件截取到本机终端中不会实际发送到目标邮箱,用于测试
# EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'