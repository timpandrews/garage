from django.contrib.auth.models import User
from django.db import models


class Doc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_type = models.CharField(max_length = 200)
    data_date = models.DateTimeField()
    data = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.data_type