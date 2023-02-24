from django.contrib.auth.models import User
from django.db import models

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

    class Meta:
        get_latest_by = "data_date"

    def __str__(self):
        return self.data_type


class Kudos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=KUDOS_TYPES,)
    data = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    placed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Kudos"

    def __str__(self):
        return self.key