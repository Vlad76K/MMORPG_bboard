from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def mmorpg_send_mail(html_content, subject, body, from_email, to_email):
    msg = EmailMultiAlternatives(
        subject=subject,        # тема
        body=body,              # сообщение с кратким описанием
        from_email=from_email,  # почта, с которой будете отправлять
        to=to_email,            # список получателей
    )
    if html_content is not None:
        msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


def mail_about_comment(post_id, post_title, client_fname, comment_text, client_email):
    link = f'http://127.0.0.1:8000/posts/{post_id}'
    appointment_message = f'Здравствуйте, {client_fname}. Новый комментарий в Вашем топике!'
    appointment_subject = f'Коментарий в топике: {post_title}'
    recipient_list = []
    recipient_list.append(client_email)

    # получаем наш html
    html_content = render_to_string(
        'post_create_notification.html',
        {
            'link' : link,
            'post_title': post_title,
            'text': appointment_message,
            'text1': comment_text,
            'appointment_subject': appointment_subject,
        }
    )
    mmorpg_send_mail(html_content, appointment_subject, appointment_message, settings.EMAIL_HOST_USER, recipient_list)
