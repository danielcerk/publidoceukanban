from django.db import models

from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):

    user = models.ForeignKey(

        User,
        verbose_name='Usuário',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='notifications'

    )

    author = models.ForeignKey(
        User,
        verbose_name='Autor',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='author'

    )

    title = models.CharField(
        verbose_name='Título',
        max_length=120,
        null=False,
        blank=True
    )

    description = models.TextField()

    is_read = models.BooleanField(
        verbose_name='Lida',
        default=False
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(
        verbose_name='Data/Hora da Notificação',
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    class Meta:

        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'


    def __str__(self):

        return self.title