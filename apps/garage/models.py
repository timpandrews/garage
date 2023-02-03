from django.db import models


class Doc(models.Model):
    user_id = models.IntegerField(default=1)
    data_type = models.CharField(max_length = 200)
    data = models.JSONField()


    def __str__(self):
        return self.data_type