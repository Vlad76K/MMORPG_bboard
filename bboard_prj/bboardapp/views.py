# Create your views here.
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.signals import post_save
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import datetime

from .forms import PostForm, CommentForm, UserImageForm, NewsForm
from .models import Post, Comment, Category, Author, News

from .my_function import mail_about_comment, mmorpg_send_mail

from django.conf import settings

from .signals import notify_about_new_post


class Categories:
    """ Выводим все категории """
    def get_category(self):
        return Category.objects.all()


class FilterPostsView(Categories, ListView):
    """ Фильтр постов """
    context_object_name = 'posts'
    template_name = "posts.html"

    def get_queryset(self):
        pc_id = Category.objects.filter(category_name__in=self.request.GET.getlist('category_name')).values_list('id')
        pc_id_list = []
        for i in pc_id:
            pc_id_list.append(i[0])
        queryset = Post.objects.filter(post_category_id__in=pc_id_list)

        return queryset


class FilterMyPostsView(Categories, ListView):
    """ Фильтр постов """
    context_object_name = 'posts'
    template_name = "posts.html"

    def get_queryset(self):
        author = Author.objects.get(author_user_id=self.request.user.id)
        queryset = Post.objects.filter(post_author_id=author.id)

        return queryset


class Search(ListView):
    """ Поиск по тексту """
    context_object_name = 'posts'
    template_name = "posts.html"
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q').capitalize()
        return Post.objects.filter(post_title__icontains=q)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class PostList(Categories, ListView):
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


# Добавляем новое представление для создания постов.
class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm               # Указываем нашу разработанную форму
    template_name = 'post_create.html'  # и новый шаблон, в котором используется форма.
    success_url = '../../../'
    permission_required = ('bboardapp.post_create', )

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm()
            img_form = UserImageForm(request.POST, request.FILES, use_required_attribute=False)
            img_object = img_form.instance
            # vdo_form = UserVideoForm(request.POST, request.FILES, use_required_attribute=False)
            # vdo_object = vdo_form.instance

            full_text = ''
            if request.FILES['post_image'] != '':
                full_text += f"<p><img alt='' src='/media/images/{request.FILES['post_image']}' style='height:400px; width:677px' /><p>{request.POST['post_text']}</p>"

            video_ref = request.POST['post_video']
            if len(video_ref) < 5:
                video_ref = ''
            else:
                full_text += f'<p><object height="360" width="640"><param name="movie" value="{video_ref}?hl=ru&amp;version=3" /><param name="allowFullScreen" value="true" /><param name="allowscriptaccess" value="always" /><embed allowfullscreen="true" allowscriptaccess="always" height="360" src="{video_ref}?hl=ru&amp;version=3" type="application/x-shockwave-flash" width="640" /></object></p>'
                full_text = full_text.replace('watch?v=', 'v/')  # меняем ссылку https://www.youtube.com/watch?v=5M_-RftEYOE (в таком виде
                                                      # не показывает ролик на странице - ругается на Adobe Flash Player)

            pst = Post(post_text=full_text,
                       post_title=request.POST['post_title'],
                       post_date=datetime.now(),
                       post_author_id=request.user.pk,
                       post_category_id=request.POST['post_category'],
                       post_image=request.FILES['post_image'],
                       post_video=video_ref)
            pst.save()

            return render(request, 'post_create.html', {'form': form, 'img_obj': img_object})
        else:
            form = self.form_class()
        return render(request, 'post_create.html', {'form': form})


class PostDetail(DetailView):
    model = Post                         # Модель всё та же, но мы хотим получать информацию по отдельному посту
    form = PostForm
    model_comment = Comment
    form_comment = CommentForm
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'  # Название объекта, в котором будет выбранный пользователем пост
    success_url = '../../posts/'

    def post(self, request, *args, **kwargs):
        this_post = Post.objects.filter(pk=self.kwargs.get('pk')).values('post_title')

        # запишем новый комментарий в базу
        cmnt = Comment(comment_text=request.POST['comment_text'],
                       comment_user_id=request.user.pk,
                       comment_post_id=self.kwargs.get('pk'))
        cmnt.save()

        # отправим автору объявления уведомление о появлении нового комментария
        mail_about_comment(self.kwargs.get('pk'),           # id объявления
                           this_post[0].get('post_title'),  # заголовок объявления
                           request.user.username,           # логин комментирующего
                           request.POST['comment_text'],    # текст комментария
                           request.user.email)              # email комментирующего

        return redirect(self.success_url)


class СheckComment(DetailView):
    model = Comment
    form = CommentForm
    template_name = 'comment_updt.html'   # Используем другой шаблон
    context_object_name = 'comment_updt'  # Название объекта, в котором будет выбранный пользователем пост
    success_url = '../../posts/'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            cmnt = Comment.objects.get(pk=self.kwargs.get('pk'))
            if 'success' in request.POST:  # обработка кнопки "Принять" коммент
                cmnt.comment_accept = 'X'
                cmnt.comment_reject = ''
                cmnt.save()

                print('!!!! settings.EMAIL_HOST_USER = ', settings.EMAIL_HOST_USER)

                mmorpg_send_mail(None,
                                 'Ваш комментарий принят', f'Ваш комментарий {cmnt.comment_text} принят',
                                 settings.EMAIL_HOST_USER,
                                 [request.user.email])
            if 'reject' in request.POST:  # обработка кнопки "Удалить" коммент
                cmnt.comment_accept = ''
                cmnt.comment_reject = 'X'
                cmnt.save()

        return redirect(self.success_url+str(cmnt.comment_post_id))


# Добавляем представление для изменения товара.
# @method_decorator(login_required, name='dispatch')
class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('bboardapp.post_update', )

    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    success_url = '../posts/'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm()
            img_form = UserImageForm(request.POST, request.FILES, use_required_attribute=False)
            img_object = img_form.instance
            # vdo_form = UserVideoForm(request.POST, request.FILES, use_required_attribute=False)
            # vdo_object = vdo_form.instance

            full_text = request.POST['post_text']
            full_text_list = request.POST['post_text'].split('<p>')
            if (len(full_text_list) > 1) and (len(request.FILES) > 0):
                full_text = full_text_list[2]
                full_text = full_text[0:len(full_text) - 4]

            if len(request.FILES) > 0:
                full_text = f"<p><img alt='' src='/media/images/{request.FILES['post_image']}' style='height:400px; width:677px' /><p>{full_text}</p>"
                         #     <p><img alt='' src='/media/images/Sargak.jpg' style='height:400px; width:677px' /><p>Убивает и врагов и союзников</p>

            video_ref = request.POST['post_video'].strip()
            if len(video_ref) > 1:
                video_ref = video_ref.replace('watch?v=', 'v/')  # меняем ссылку https://www.youtube.com/watch?v=5M_-RftEYOE (в таком виде
                                                                 # не показывает ролик на странице - ругается на Adobe Flash Player)
                full_text += f'<p><object height="360" width="640"><param name="movie" value="{video_ref}?hl=ru&amp;version=3" /><param name="allowFullScreen" value="true" /><param name="allowscriptaccess" value="always" /><embed allowfullscreen="true" allowscriptaccess="always" height="360" src="{video_ref}?hl=ru&amp;version=3" type="application/x-shockwave-flash" width="640" /></object></p>'

            pst = Post.objects.get(pk=self.kwargs.get('pk'))
            pst.post_text = full_text
            pst.post_title = request.POST['post_title']
            pst.post_date = datetime.now()
            pst.post_category_id = request.POST['post_category']
            if len(request.FILES) > 0:
                pst.post_image = request.FILES['post_image']
            if video_ref != '':
                pst.post_video = video_ref
            pst.save()

            return render(request, 'post_create.html', {'form': form, 'img_obj': img_object})
        else:
            form = self.form_class()
        return redirect(self.success_url)


class NewsListView(ListView):
    # success_url = 'post_update.html'

    model = News
    queryset = News.objects.all()

    ordering = '-news_date'
    context_object_name = 'news'
    template_name = "news.html"


class NewsAddView(CreateView):
    form_class = NewsForm               # Указываем нашу разработанную форму
    template_name = 'news_create.html'  # и новый шаблон, в котором используется форма.
    success_url = '../../../news'

    def post(self, request, *args, **kwargs):
        form = NewsForm()
        if request.method == 'POST':
            full_text = request.POST['news_text']
            if len(request.FILES) > 0:
                full_text = f"<p><img alt='' src='/media/images/{request.FILES['news_image']}' style='height:400px; width:677px' /><p>{full_text}</p>"
            news = News(news_text=full_text,
                        news_title=request.POST['news_title'],
                        news_date=datetime.now(),
                        news_author_id=request.user.pk,
                        news_image=request.FILES['news_image'])
            news.save()

            post_save.connect(notify_about_new_post, sender=News)

        return render(request, 'news_create.html', {'form': form})

class NewsDetail(DetailView):
    model = News                         # Модель всё та же, но мы хотим получать информацию по отдельному посту
    form = NewsForm
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'  # Название объекта, в котором будет выбранный пользователем пост
    success_url = '../../news/'

