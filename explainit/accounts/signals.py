from django.db.models.signals import post_save
from .models import Account, ProfilePic
from django.dispatch import receiver

@receiver(post_save, sender=Account)
def CreateUserAccount(sender, instance, created, **kwargs):
    if created:
        ProfilePic.objects.create(user=instance)
