from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Board(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="boards_as_author",
        null=True,
        blank=True
    )

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