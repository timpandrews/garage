from django.db.models import signals
from django.dispatch import receiver
from .models import Kudos

@receiver(signals.post_save, sender=Kudos)
def create_hexkey(sender, instance, created, **kwargs):
    hexnum = hex(instance.id)[2:].zfill(6)
    Kudos.objects.filter(pk=instance.id).update(hex=hexnum)