from django.db import models


class Word(models.Model):
    title = models.CharField(max_length=20)
    html = models.TextField(default='')
