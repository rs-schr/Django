from django.db import models

# Create your models here.
class Past(models.Model):
    question = models.CharField(max_length=250)
    response = models.TextField(max_length=25000)

    def __str__(self):
        return self.question




