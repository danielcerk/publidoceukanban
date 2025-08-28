from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from .models import Board

User = get_user_model()

@receiver(post_save, sender=User)
def create_board_user(sender, instance, created, **kwargs):
    
    if created and not instance.is_staff and not instance.is_superuser:

        if not Board.objects.filter(customer=instance).exists():
            
            Board.objects.create(customer=instance)
		