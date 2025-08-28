from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Board(models.Model):

    customer = models.ForeignKey(

        User, on_delete=models.CASCADE,
        verbose_name='Cliente',
        null=False, blank=False

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

        verbose_name = 'Quadro'

    def __str__(self):

        return f'Quadro de {self.customer}'