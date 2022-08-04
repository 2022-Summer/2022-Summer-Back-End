from django.db import models


class Word(models.Model):
    html = models.TextField(default='')
