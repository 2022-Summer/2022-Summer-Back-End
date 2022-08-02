from django.db import models


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'headshot.' + ext
    return 'user_{0}/headshot/{1}'.format(instance.id, filename)


class User(models.Model):
    mailbox = models.EmailField(unique=True, default='')
    username = models.CharField(max_length=20)
    real_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20, default='')
    description = models.CharField(max_length=255, default='')
    headshot = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
