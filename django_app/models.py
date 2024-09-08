from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class Profile(models.Model):

    user = models.OneToOneField(
        verbose_name="Пользователь",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=True,
        default=None,
        max_length=300,
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    mail_login = models.CharField(
        verbose_name="Логин почты",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=30,
    )

    mail_password = models.CharField(
        verbose_name="Пароль почты",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=100,
    )

    def __str__(self):
        return f"<Profile [{self.user.id}]{self.user.username}>"


@receiver(post_save, sender=User)
def profile_create(sender, instance: User, created: bool, **kwargs):
    profile = Profile.objects.get_or_create(user=instance)


class Message(models.Model):

    user = models.ForeignKey(
        verbose_name="Автор",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=100,
        to=User,
        on_delete=models.CASCADE,
    )

    author = models.CharField(
        verbose_name="Автор сообщения",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        max_length=100,
    )

    topic = models.CharField(
        verbose_name="Тема",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        max_length=100,
    )

    date_send = models.DateTimeField(
        verbose_name="Дата отправки ",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        max_length=100,
    )

    date_added = models.DateTimeField(
        verbose_name="Дата получения",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default=timezone.now,
    )
    text = models.TextField(
        verbose_name="Текст",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=True,
        default=None,
    )
