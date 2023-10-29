from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField


# категории объявлений
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)  # - название категории.

    def __str__(self):
        return self.category_name


# авторы объявлений
class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)  # - cвязь «один к одному» с встроенной моделью пользователей User

    def __str__(self):
        return self.author_user.username


class UploadImage(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.caption


class UploadVideo(models.Model):
    caption = models.CharField(max_length=200)
    image = models.FileField(upload_to='video')

    def __str__(self):
        return self.caption


# объявления
class Post(models.Model):
    post_author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)  # - связь «один ко многим» с моделью Author;
    post_category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, default=0)  # - связь «один ко многим» с моделью Category;
    post_date = models.DateTimeField('Дата', auto_now_add=datetime.now())                    # - автоматически добавляемая дата и время создания;
    post_title = models.CharField('Заголовок', max_length=124)          # - заголовок;
    post_text = RichTextUploadingField(verbose_name='Полный текст статьи', help_text='Тут нужно ввести всю статью в формате HTML')
    post_image = models.ImageField(upload_to='images')
    post_video = models.CharField('Ссылка на видео', max_length=500)
    # post_video = models.FileField(upload_to='video')

    # - Метод preview(), который возвращает начало поста (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        return str(self.post_text)[0:125] + '...'

    # def __str__(self):
    #     return str(self.value)


# комментарии пользователей к объявлению
class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)     # - связь «один ко многим» с моделью Post;
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)     # - связь «один ко многим» со встроенной моделью User;
    comment_text = models.TextField()                                             # - текст комментария;
    comment_datetime = models.DateTimeField(auto_now_add=datetime.now())  # - дата и время создания комментария;
    comment_accept = models.CharField(max_length=2, default='')  # - =X, если коммент акцептован;
    comment_reject = models.CharField(max_length=2, default='')  # - =X, если коммент удален;

    def __str__(self):
        return f"{self.comment_text} - {self.comment_post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


# Коды подтверждения (например: при регистрации пользователя)
class CodeConfirmation(models.Model):
    code_confirmation = models.CharField(max_length=20, default='')
    code_confirmation_datetime = models.DateTimeField(auto_now_add=datetime.now())
    code_confirmation_type = models.IntegerField(default=0)
    code_confirmation_email = models.CharField(max_length=200, default='')

# объявления
class News(models.Model):
    news_author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)  # - связь «один ко многим» с моделью Author;
    news_date = models.DateTimeField('Дата', auto_now_add=datetime.now())                    # - автоматически добавляемая дата и время создания;
    news_title = models.CharField('Заголовок', max_length=124)          # - заголовок;
    news_text = RichTextUploadingField(verbose_name='Полный текст новости')
    news_image = models.ImageField(upload_to='images')

    # - Метод preview(), который возвращает начало поста (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        return str(self.news_text)[0:125] + '...'
