from django.db import models

class Doc(models.Model):
    doc_id = models.Field(primary_key = True)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title