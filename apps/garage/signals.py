from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Doc, Kudos, Profile


@receiver(post_save, sender=Kudos)
def create_hexkey(sender, instance, created, **kwargs):
    """
    Create a hexadecimal key based on the instance's ID and user ID.
    
    Args:
        sender: The sender of the signal.
        instance: The instance that triggered the signal.
        created: A boolean indicating if the instance was created or updated.
        **kwargs: Additional keyword arguments.
    """
    
    hexid = hex(instance.id)[2:].zfill(6)
    hexuser = hex(instance.user_id)[2:].zfill(3)
    key = f"{hexuser}_{hexid}"
    Kudos.objects.filter(pk=instance.id).update(hex=hexid, key=key)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Update the user profile.

    This function is called when a user is created. It creates a profile for the user
    and sets the initial habit.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user being created.
        created: A boolean indicating whether the user is being created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance, habits={"habit1": "Be Kind"})
        instance.profile.save()


@receiver(post_save, sender=User)
def create_first_activity(sender, instance, created, **kwargs):
    """
    Create a first activity for a user when the user is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user being created.
        created: A boolean indicating whether the user is being created or not.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
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
