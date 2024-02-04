import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import UserAccount


@receiver(pre_delete, sender=UserAccount)
def delete_profile_images(sender, instance, **kwargs):
    file_path = instance.profile_picture.path
    if os.path.exists(file_path):
        os.remove(file_path)
