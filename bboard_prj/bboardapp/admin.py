from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Author, Comment, Category, News


class PostAdminForm(forms.ModelForm):
    post_text = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = ['post_author', 'post_title', 'post_text', 'post_category']

class PostAdmin(admin.ModelAdmin):
    form_class = PostAdminForm
    model = Post

# @admin.register(Post) #Movie)
# class MovieAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Post)
admin.site.register(News)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
# admin.site.register(PostAdmin)
