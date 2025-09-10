from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from api.card.models import Card, Feedback
from .models import Notification


def create_notification_and_email(user, author, description, title='Notificação do sistema'):

    Notification.objects.create(
        user=user,
        author=author,
        description=description
    )

    if user.email:

        send_mail(
            subject=title,
            message=description,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )



@receiver(post_save, sender=Card)
def notify_card_user(sender, instance, created, **kwargs):

    if created:

        description = f'Novo card criado para o cliente {instance.board.customer}'

        create_notification_and_email(
            user=instance.board.customer,
            author=instance.board.user,
            description=description,
            title='Novo Card Criado'
        )

    else:

        if 'status' in instance.get_deferred_fields():

            description = f'O status do card {instance.id} foi alterado para {instance.status}'
            create_notification_and_email(
                user=instance.board.customer,
                author=instance.board.user,
                description=description,
                title='Status do Card Atualizado'
            )


@receiver(post_save, sender=Feedback)
def notify_feedback_admin(sender, instance, created, **kwargs):

    if created:

        pass

    else:

        description = f'O feedback de {instance.board.customer} foi atualizado'

        create_notification_and_email(
            user=instance.board.user,
            author=instance.board.customer,
            description=description,
            title='Feedback Atualizado'
        )
