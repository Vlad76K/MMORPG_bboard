from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import News, User


def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string("post_create_notification.html",
                                    {"text": preview, "link": f"{settings.SITE_URL}/news/{pk}"})
    msg = EmailMultiAlternatives(subject=title, body="", from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers, )
    msg.attach_alternative(html_context, "text/html")
    msg.send()


@receiver(post_save, sender=News)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created:  # в случае создания новости оправляем письма всем зарегистрированным пользователям
        usr_all = User.objects.all()
        subscribers = []
        for fnd in usr_all:
            if len(fnd.email) > 0:
                subscribers.append(fnd.email)
        send_notification(instance.preview(), instance.pk, instance.news_title, subscribers)
    else:  #если потребуется обабатывать обновление новостей
        pass
