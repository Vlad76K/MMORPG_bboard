# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from datetime import datetime

from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post                  # Указываем модель, объекты которой мы будем выводить
    ordering = '-post_date'       # Поле, которое будет использоваться для сортировки объектов
    template_name = 'posts.html'   # Указываем имя шаблона, в котором будут все инструкции о том,
                                  # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'posts'  # Это имя списка, в котором будут лежать все объекты.
                                  # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 5               # Количество объявлений на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_action'] = "Творческий вечер в среду!"
        return context


class PostDetail(DetailView):
    model = Post                      # Модель всё та же, но мы хотим получать информацию по отдельному посту
    template_name = 'post_detail.html'   # Используем другой шаблон — post.html
    context_object_name = 'post_detail'  # Название объекта, в котором будет выбранный пользователем пост


# Добавляем новое представление для создания постов.
class PostCreate(CreateView):
    form_class = PostForm               # Указываем нашу разработанную форму
    model = Post                        # модель постов
    template_name = 'post_create.html'  # и новый шаблон, в котором используется форма.
    success_url = '../../../'
    permission_required = ('bboardapp.post_create', )

