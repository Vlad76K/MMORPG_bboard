from datetime import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.core.exceptions import ValidationError
from django import forms
from .models import Post, Comment, UploadImage, UploadVideo, News


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = '__all__'


class UserVideoForm(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = '__all__'


class PostForm(forms.ModelForm):
    post_text = forms.CharField(widget=CKEditorUploadingWidget(), initial='CKEditorUploadingWidget !!!', help_text='Тут нужно ввести всю статью в формате HTML')
    post_date = datetime.now()
    post_author = forms.IntegerField()

    class Meta:
        model = Post
        fields = ['post_author', 'post_title', 'post_text', 'post_category', 'post_image', 'post_video']

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get('post_text')
        post_title = cleaned_data.get('post_title')
        if str(post_text) == str(post_title):
            raise ValidationError({'post_title': "Заголовок не должен быть идентичен тексту."})

        return cleaned_data


class NewsForm(forms.ModelForm):
    news_text = forms.CharField(widget=CKEditorUploadingWidget(), initial='CKEditorUploadingWidget !!!', help_text='Тут нужно ввести всю статью в формате HTML')
    news_date = datetime.now()
    # news_author = forms.IntegerField()

    class Meta:
        model = News
        fields = ['news_author', 'news_title', 'news_text', 'news_image']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text', 'comment_post', 'comment_user']
