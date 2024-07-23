from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

# Conectar a criação de usuário com post_save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    # Se foi criado e não atualizado
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()