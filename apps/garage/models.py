from django.contrib.auth.models import User
from django.db import models


KUDOS_TYPES = (
    ("App", "app"), # Application Kudos
    ("Rides", "rides"),
    ("HP", "hp"), # health points
)

class Doc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length = 200)
    doc_date = models.DateTimeField()
    data = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    kudosed = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "doc_date"

    def __str__(self):
        return self.doc_type


class Kudos(models.Model):
    hex = models.CharField(max_length=8, blank=True) # value set in signals.create_hexkey()
    key = models.CharField(max_length=20, blank=True) # value set in signals.create_hexkey()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=KUDOS_TYPES,)
    data = models.JSONField(blank=True, default=dict)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    placed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Kudos"

    def __str__(self):
        return self.key


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'