from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Recipe

import os

def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...
        
@receiver(pre_delete, sender=Recipe)
def recipe_delete(sender, instance, *args, **kwargs):
    delete_cover(instance)
        
@receiver(pre_save, sender=Recipe)
def recipe_update(sender, instance, *args, **kwargs):
    if instance.pk:
        old_instance = Recipe.objects.get(pk=instance.pk)
        is_new = old_instance.cover != instance.cover

        if is_new:
            delete_cover(old_instance)


