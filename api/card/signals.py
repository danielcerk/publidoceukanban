from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from api.supabase_utils import delete_from_supabase

from .models import Card, Feedback


@receiver(pre_delete, sender=Card)
def delete_card_files_from_supabase(sender, instance, **kwargs):
    arquivos = instance.files.all() 

    for arquivo in arquivos:
        if arquivo.file and "supabase.co" in arquivo.file:
            delete_from_supabase(arquivo.file)

