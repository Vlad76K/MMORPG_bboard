import random
from datetime import datetime
from django import template
from django.core.mail import send_mail

# from .models import Comment

register = template.Library()


@register.simple_tag()
def current_time(format_string='%b %d %Y %A'):
   return datetime.utcnow().strftime(format_string)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()


@register.simple_tag(takes_context=True)
def send_code_confirm1(context, **kwargs):
    print('!!!!!!! send_code_confirm ======= ')
    d = context['request'].GET.copy()
    print('!!!!!!! send_code_confirm ======= ', d)
    for k, v in kwargs.items():
        d[k] = v
        print('!!!!!!! send_code_confirm ======= ', v)


@register.simple_tag()
def send_code_confirm(cc_code, cc_email):
    if cc_email is not None:
        cc_code = random.choice('abcde')
        send_mail(
            subject='Регистрация на сайте MMORPG',  # Категория и дата записи будут в теме для удобства
            message='Код подтверждения регистрации: ' + cc_code,  # сообщение с кратким описанием
            from_email='Kornyushin.Vladislav@yandex.ru',  # здесь указываете почту, с которой будете отправлять
            recipient_list=[cc_email]  # здесь список получателей
        )

    return ''


@register.simple_tag()
def your_custom_tag_django1(cc_code, cc_email):
    pass
