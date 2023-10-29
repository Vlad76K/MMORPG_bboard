# Generated by Django 4.2.6 on 2023-10-24 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboardapp', '0014_alter_post_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_video',
            field=models.FileField(default='', upload_to='video'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bboardapp.category', verbose_name='Категория'),
        ),
    ]
