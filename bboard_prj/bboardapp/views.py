# Create your views here.
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import datetime

from .forms import PostForm, CommentForm
from .models import Post, Comment
from .my_function import mail_data_fill

# class CkEditorFormView(generic.FormView):
#     form_class = forms.CkEditorForm
#     template_name = "form.html"
#
#     def get_success_url(self):
#         return reverse("ckeditor-form")
#
#
# class CkEditorMultiWidgetFormView(generic.FormView):
#     form_class = forms.CkEditorMultiWidgetForm
#     template_name = "form.html"
#
#     def get_success_url(self):
#         return reverse("ckeditor-multi-widget-form")
#
#
# ckeditor_form_view = CkEditorFormView.as_view()
# ckeditor_multi_widget_form_view = CkEditorMultiWidgetFormView.as_view()


class PostList(ListView):
    model = Post                   # Указываем модель, объекты которой мы будем выводить
    ordering = '-post_date'        # Поле, которое будет использоваться для сортировки объектов
    template_name = 'posts.html'   # Указываем имя шаблона, в котором будут все инструкции о том,
                                   # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'posts'  # Это имя списка, в котором будут лежать все объекты.
                                   # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.

    model.post_text = forms.CharField(widget=CKEditorWidget())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_action'] = "Творческий вечер в среду!"

        return context


class PostDetail(DetailView):
    model = Post                         # Модель всё та же, но мы хотим получать информацию по отдельному посту
    template_name = 'post_detail.html'   # Используем другой шаблон — post.html
    context_object_name = 'post_detail'  # Название объекта, в котором будет выбранный пользователем пост


# Добавляем новое представление для создания постов.
class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm               # Указываем нашу разработанную форму
    model = Post                        # модель постов
    template_name = 'post_create.html'  # и новый шаблон, в котором используется форма.
    model.post_text = forms.CharField(widget=CKEditorWidget())
    success_url = '../../../'
    permission_required = ('bboardapp.post_create', )


class PostUpdate(LoginRequiredMixin, UpdateView):  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    permission_required = ('bboardapp.post_update', )

    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    success_url = '../posts/'

    def form_valid(self, form):
        if form.is_valid():
            form.save(commit=False)
            # отправим подписчикам уведомление о появлении новой публикации
            mail_data_fill(self.request, self.success_url)

        return super().form_valid(form)

class AddComment(LoginRequiredMixin, UpdateView):
    template_name = 'comment_create.html'
    success_url = '../posts/'
    context_object_name = 'comment_create'

    def post(self, request, pk):
        form = CommentForm
        # post_model = Post.objects.get(id=pk)
        if form.is_valid():
            form.save(commit=False)
            form.comment_post_id = pk
            form.save()

            # отправим подписчикам уведомление о появлении новой публикации
            mail_data_fill(self.request, self.success_url)

        return redirect(self.success_url)

    # form_class = CommentForm
    # model = Comment
    # template_name = 'comment_create.html'
    # success_url = '../posts/'
    # context_object_name = 'comment_create'
    #
    # def form_valid(self, form):
    #     if form.is_valid():
    #         form.save(commit=False)
    #         # отправим подписчикам уведомление о появлении новой публикации
    #         # mail_data_fill(self.request, self.success_url)
    #
    #     return super().form_valid(form)
