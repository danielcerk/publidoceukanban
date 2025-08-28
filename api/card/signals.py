from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Card, Feedback

@receiver(post_save, sender=Card)
def create_feedback_card(sender, instance, created, **kwargs):
    
    if created and not Feedback.objects.filter(card=instance).exists():

        Feedback.objects.create(
            card=instance
        )
		