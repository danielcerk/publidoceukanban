from django.db import models
from django.utils import timezone
from datetime import timedelta
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

    approved_date = models.DateField(
        verbose_name='Data de aprovação',
        null=True,
        blank=True
    )
    
    deleted_at = models.DateField(
        verbose_name='Data de exclusão',
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

        if self.pk:

            old_status = Card.objects.filter(pk=self.pk).values_list("status", flat=True).first()

        else:

            old_status = None

        if self.status == "done":

            self.approved_date = timezone.now().date()
            self.deleted_at = self.approved_date + timedelta(days=30)

        elif old_status == "done" and self.status != "done":
            
            self.approved_date = None
            self.deleted_at = None

        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):

        return self.title

class FileCard(models.Model):

    card = models.ForeignKey(

        Card, on_delete=models.CASCADE,
        verbose_name='Card',
        null=False, blank=False,
        related_name="files",

    )

    is_approved = models.BooleanField(

        verbose_name='Está aprovado',
        null=True, blank=True,
        default=False

    )

    file = models.URLField(
         
         verbose_name='Arquivo',
         default='https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png'

    )

    class Meta:

        verbose_name = 'Arquivo do Card'
        verbose_name_plural = 'Arquivos de Cards'

    def __str__(self):

        return f'Arquivo {self.id} ref. {self.card.title}'
    
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