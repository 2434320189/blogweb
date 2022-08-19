from django.contrib import admin
from .models import SideBar
from .models import Category, Post, Tag

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(SideBar)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','tags','owner','is_hot','pub_date')
    list_filter = ('owner',)
    search_fields = ('title','desc')
    list_editable = ('is_hot',)
    list_display_links = ('title',)

    class Media:

        css={'all': ('ckeditor5/cked.css'),}

        js= (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor5/build/ckeditor.js',
            'ckeditor5/build/translations/zh.js',
            'ckeditor5/config.js',
        )

admin.site.register(Post,PostAdmin)
