from datetime import datetime

from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget
from ckeditor_demo.demo_application.widgets import CkEditorMultiWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.core.exceptions import ValidationError
from django import forms
from django.http import HttpResponseRedirect

from .models import Post, Comment, User


class CkEditorForm(forms.Form):
    ckeditor_standard_example = RichTextFormField()
    # ckeditor_upload_example = RichTextUploadingFormField(config_name="my-custom-toolbar")


class CkEditorMultiWidgetForm(forms.Form):
    pass
    # SUBWIDGET_SUFFIXES = ["0", "1"]
    #
    # ckeditor_standard_multi_widget_example = forms.CharField(
    #     widget=CkEditorMultiWidget(
    #         widgets={suffix: CKEditorWidget for suffix in SUBWIDGET_SUFFIXES},
    #     ),
    # )
    # ckeditor_upload_multi_widget_example = forms.CharField(
    #     widget=CkEditorMultiWidget(
    #         widgets={
    #             suffix: CKEditorUploadingWidget(config_name="my-custom-toolbar")
    #             for suffix in SUBWIDGET_SUFFIXES
    #         },
    #     ),
    # )


class PostForm(forms.ModelForm):
    post_text = forms.CharField(widget=CKEditorWidget(), help_text='Тут нужно ввести всю статью в формате HTML')

    comment_text = forms.CharField(widget=CKEditorWidget(), help_text='Тут нужно ввести свой коммент в формате HTML')

    class Meta:
        model = Post
        fields = ['post_author', 'post_title', 'post_text', 'post_category']

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get('post_text')
        post_title = cleaned_data.get('post_title')
        if str(post_text) == str(post_title):
            raise ValidationError({
                'post_title': "Заголовок не должен быть идентичен тексту."
            })

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

    def post(self, request, *args, **kwargs):
        subscribes = Comment(comment_text=self.comment_text,
                             comment_datetime=datetime.now(),
                             comment_post_id=Post.objects.get(pk=1),
                             comment_user_id=User.objects.get(pk=request.user.pk), )
        subscribes.save()
        return HttpResponseRedirect('../posts/', request)

