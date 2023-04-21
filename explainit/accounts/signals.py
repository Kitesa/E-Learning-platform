from django.db.models.signals import post_save
from .models import Account, ProfilePic, UserBio
from django.dispatch import receiver

@receiver(post_save, sender=Account)
def CreateUserAccount(sender, instance, created, **kwargs):
    if created:
        ProfilePic.objects.create(user=instance)
        UserBio.objects.create(user=instance)
