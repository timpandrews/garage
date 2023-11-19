from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Doc, Kudos, Profile


@receiver(post_save, sender=Kudos)
def create_hexkey(sender, instance, created, **kwargs):
    hexid = hex(instance.id)[2:].zfill(6)
    hexuser = hex(instance.user_id)[2:].zfill(3)
    key = f"{hexuser}_{hexid}"
    Kudos.objects.filter(pk=instance.id).update(hex=hexid, key=key)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    print("update_user_profile")
    # Create a profile for a user when the user is created
    if created:
        Profile.objects.create(user=instance, habits={"habit1": "Be Kind"})
        instance.profile.save()


@receiver(post_save, sender=User)
def create_first_activity(sender, instance, created, **kwargs):
    # create a first activity for a user when the user is created
    if created:
        dt = datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        Doc.objects.create(
            user=instance,
            doc_type="joined",
            doc_date=dt,
        )


# TODO: create signal to create a trophy for joining the site, cause everyone gets a trophy!
# def create_welcome_to_the_site_trophy...
