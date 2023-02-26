from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

KUDOS_TYPES = (
    ("App", "app"), # Application Kudos
    ("Rides", "rides"),
    ("HP", "hp"), # health points
)


class Doc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_type = models.CharField(max_length = 200)
    data_date = models.DateTimeField()
    data = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    kudosed = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "data_date"

    def __str__(self):
        return self.data_type


class Kudos(models.Model):
    hex = models.CharField(max_length=8, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=20) # value set in signals.create_hexkey()
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
