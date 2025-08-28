from django.db import models
from api.board.models import Board
from django.core.exceptions import ValidationError

class Card(models.Model):

    STATUS_CHOICES = [
        ('todo', 'A Fazer'),
        ('in_progress', 'Em Progresso'),
        ('review', 'Em Revisão'),
        ('done', 'Concluído'),
        ('disapprove', 'Reprovado'),
    ]

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE,
        verbose_name='Cliente',
        null=False, blank=False
    )

    title = models.CharField(
        verbose_name='Título',
        max_length=155,
        null=False,
        blank=True
    )

    description = models.TextField(
        
        verbose_name='Descrição',
        null=True,
        blank=True

    )

    image = models.URLField(

        verbose_name='Imagem',
        default='https://storage.googleapis.com/star-lab/blog/OGs/image-not-found.png',
        null=True, blank=True

    )

    status = models.CharField(
        verbose_name='Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    is_active = models.BooleanField(
        verbose_name='Está ativo',
        default=True
    )

    start_date = models.DateField(
        verbose_name='Data de início',
        null=True,
        blank=True
    )

    due_date = models.DateField(
        verbose_name='Data de entrega',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    def clean(self):

        if self.start_date and self.due_date:

            if self.due_date < self.start_date:

                raise ValidationError(

                    {'due_date': 'A data de entrega não pode ser anterior à data de início.'}

                )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title
    
class Feedback(models.Model):

    card = models.OneToOneField(
        Card, on_delete=models.CASCADE,
        verbose_name='Card',
        null=False, blank=False,
    )

    text = models.TextField(
        
        verbose_name='Descrição',
        null=True,
        blank=True

    )

    class Meta:

        verbose_name = 'Feedback do card'
        verbose_name_plural = 'Feedbacks dos cards'

    def __str__(self):

        return f'Feedback ref. {self.card.title}'