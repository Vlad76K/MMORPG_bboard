import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

from .models import Comment, Post, Author


def mail_notification_post_create(link, appointment_title, appointment_message, appointment_message1, appointment_subject, recipient_list, client_username):
    # получаем наш html
    html_content = render_to_string(
        'post_create_notification.html',
        {
            'link' : link,
            'post_title': appointment_title,
            'text': appointment_message,
            'text1': appointment_message1,
            'appointment_subject': appointment_subject,
        }
    )

    msg = EmailMultiAlternatives(
        # тема
        subject=appointment_subject,
        # сообщение с кратким описанием
        body=appointment_message + ' --- ' + appointment_message1,
        # почта, с которой будете отправлять
        from_email='Kornyushin.Vladislav@yandex.ru',
        # список получателей
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

def mail_data_fill(request, success_url):
    client_username_lst = []

    # Для проверки в shell
    # from bboardapp.models import Comment, Post
    # p = Post.objects.filter(post_author=2).values('id')
    # p = p[0].get('id')
    # c = Comment.objects.filter(comment_post_id=p).values('comment_text')
    # c[0].get('comment_text')

    # # отправляем письмо
    post_author_id = request.POST['post_author']
    if int(post_author_id) > 0:
        qs_post = Post.objects.filter(post_author=post_author_id).values('id')
        qs_author = Author.objects.filter(pk=post_author_id).values('author_user_id')
        if qs_author.exists():
            qs_comment = Comment.objects.filter(comment_post_id=qs_post[0].get('id'))
            if qs_comment.exists():
                qs_user = User.objects.filter(pk=post_author_id).values('username', 'email', 'last_name', 'first_name')
                client_username = qs_user[0].get("username")  # логин подписчика
                client_username_lst.append(client_username)
                client_fname = qs_user[0].get("first_name")  # имя подписчика
                client_lname = qs_user[0].get("last_name")  # фамилия подписчика
                client_email = qs_user[0].get('email')  # почта подписчика
                # тема письма
                appointment_title = request.POST["post_title"]
                # текст письма
                appointment_message = f'Здравствуйте, {client_fname}. Новая статья в Вашем топике!'
                # список адресов получателей рассылки
                recipient_list = []
                recipient_list.append(client_email)
                link = f'http://127.0.0.1:8000/posts/{qs_post[0].get("id")}'
                appointment_subject = f'Коментарий в топике: {request.POST["post_title"]}'
                appointment_message1 = ' '
                for ac_id in qs_comment.values():
                    appointment_message1 += ac_id.get('comment_text')+'<br>'  #!!! Возможна дополнительная фильтрация

                mail_notification_post_create(link, appointment_title, appointment_message, appointment_message1,
                                              appointment_subject, recipient_list, client_username)

    return HttpResponseRedirect(success_url, request)

def comment_save(post_id, user_id, comment_text):
    comment_text = comment_text
    comment_datetime = datetime.datetime.now()
    comment_post_id = post_id
    comment_user_id = user_id

