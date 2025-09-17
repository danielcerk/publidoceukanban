from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from api.card.models import Card, Feedback
from .models import Notification

from django.contrib.contenttypes.models import ContentType


def create_notification_and_email(user, author, 
    description, content_type, object_id, title='Notificação do sistema'):

    Notification.objects.create(
        title=title,
        user=user,
        author=author,
        description=description,
        content_type=content_type,
        object_id=object_id
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
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            title='Novo Card Criado'
        )
    else:
        if 'status' in instance.get_deferred_fields():
            description = f'O status do card {instance.id} foi alterado para {instance.status}'
            create_notification_and_email(
                user=instance.board.customer,
                author=instance.board.user,
                description=description,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.id,
                title='Status do Card Atualizado'
            )


@receiver(post_save, sender=Feedback)
def notify_feedback_admin(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        description = f'O feedback de {instance.card.board.customer} foi atualizado'
        create_notification_and_email(
            user=instance.card.board.user,
            author=instance.card.board.customer,
            description=description,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            title='Feedback Atualizado'
        )
