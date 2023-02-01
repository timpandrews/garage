from django.db import models


class Doc(models.Model):
    title = models.CharField(max_length = 200)
    text = models.TextField()
    char = models.CharField(max_length = 200)

    def __str__(self):
        return self.title