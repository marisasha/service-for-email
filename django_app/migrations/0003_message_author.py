# Generated by Django 5.1.1 on 2024-09-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Автор сообщения'),
        ),
    ]
