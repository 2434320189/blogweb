# Generated by Django 4.0.6 on 2022-07-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='pv',
        ),
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='浏览量'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, '搜索'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论'), (5, '文章归档'), (6, '推荐文章'), (7, 'HTML')], default=1, verbose_name='展示类型'),
        ),
    ]