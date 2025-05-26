import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings

from .models import User


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    """Удаляет старый аватар при загрузке нового."""
    if not instance.pk:
        return

    try:
        old_instance = User.objects.get(pk=instance.pk)
        old_avatar = old_instance.avatar
        new_avatar = instance.avatar

        if old_avatar and old_avatar != new_avatar:
            old_avatar_path = os.path.join(
                settings.MEDIA_ROOT,
                str(old_avatar)
            )
            if os.path.isfile(old_avatar_path):
                os.remove(old_avatar_path)
    except User.DoesNotExist:
        pass
