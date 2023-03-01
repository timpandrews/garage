from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from .models import Kudos, Profile


@receiver(signals.post_save, sender=Kudos)
def create_hexkey(sender, instance, created, **kwargs):
    hexid = hex(instance.id)[2:].zfill(6)
    hexuser = hex(instance.user_id)[2:].zfill(3)
    key = f"{hexuser}_{hexid}"
    Kudos.objects.filter(pk=instance.id).update(hex=hexid, key=key)


@receiver(signals.post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
