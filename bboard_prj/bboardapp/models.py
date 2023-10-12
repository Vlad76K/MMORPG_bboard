from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy
from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
# from ckeditor.fields import RichTextField

# категории объявлений с возможностью подписки (?)
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)  # - название категории.

    def __str__(self):
        return self.category_name


# авторы объявлений с возможностью рейтингования (?)
class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)  # - cвязь «один к одному» с встроенной моделью пользователей User
    # author_rating = models.IntegerField(default=0)                      # - рейтинг пользователя

    def __str__(self):
        return self.author_user.username


# объявления с возможностью рейтингования (?)
class Post(models.Model):
    post_author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)  # - связь «один ко многим» с моделью Author;
    post_date = models.DateTimeField(auto_now_add=datetime.now())            # - автоматически добавляемая дата и время создания;
    post_category = models.ManyToManyField(Category, through='PostCategory',
                     verbose_name=pgettext_lazy('help text for Post model',
                                                'This is the help text'))    # - связь «многие ко многим» с моделью Category
                                                                             # (с дополнительной моделью PostCategory);
    post_title = models.CharField(verbose_name='Заголовок', max_length=124)  # - заголовок;

    post_text = RichTextUploadingField(verbose_name='Полный текст статьи', help_text='Тут нужно ввести всю статью в формате HTML')

    # - Метод preview(), который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        return str(self.post_text)[0:125] + '...'


# Промежуточная модель для связи «многие ко многим»:
class PostCategory(models.Model):
    post_connection = models.ForeignKey(Post, on_delete=models.CASCADE)          # - связь «один ко многим» с моделью Post;
    category_connection = models.ForeignKey(Category, on_delete=models.CASCADE)  # - связь «один ко многим» с моделью Category.


# комментарии пользователей к объявлению с возможностью рейтингования (?)
class Comment(models.Model):
    comment_post = models.ForeignKey(Post, verbose_name='Топик', on_delete=models.CASCADE)      # - связь «один ко многим» с моделью Post;
    comment_user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)      # - связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    comment_text = models.TextField('Комментарий')                                     # - текст комментария;
    comment_datetime = models.DateTimeField(verbose_name='Дата', auto_now_add=datetime.now())  # - дата и время создания комментария;

    def __str__(self):
        return f"{self.comment_text} - {self.comment_post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
