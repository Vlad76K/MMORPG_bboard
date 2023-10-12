# from celery import shared_task
#
# from django.core.mail import EmailMultiAlternatives, mail_admins
# from django.template.loader import render_to_string
#
# from .models import Post
#
# @shared_task
# def mail_notification_post_create(link, appointment_title, appointment_message, appointment_message1, appointment_subject, recipient_list, client_username):
#     # получаем наш html
#     html_content = render_to_string(
#         'post_create_notification.html',
#         {
#             'link' : link,
#             'post_title': appointment_title,
#             'text': appointment_message,
#             'text1': appointment_message1,
#             'appointment_subject': appointment_subject,
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         # тема
#         subject=appointment_subject,
#         # сообщение с кратким описанием
#         body=appointment_message,
#         # почта, с которой будете отправлять
#         from_email='Kornyushin.Vladislav@yandex.ru',
#         # список получателей
#         to=recipient_list,
#     )
#     msg.attach_alternative(html_content, "text/html")  # добавляем html
#     msg.send()  # отсылаем
#
#     # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
#     mail_admins(
#          subject=f'Клиенту {client_username} отправлено письмо: {appointment_subject}',
#          message=appointment_message,
#     )
