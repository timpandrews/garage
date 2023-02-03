from django.db import models


class Doc(models.Model):
    title = models.CharField(max_length = 200)
    user_id = models.IntegerField(default=1)
    data = models.JSONField()


    def __str__(self):
        return self.title