# Generated by Django 4.2.6 on 2023-10-15 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboardapp', '0004_codeconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeconfirmation',
            name='code_confirmation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 15, 22, 0, 42, 393937)),
        ),
    ]
