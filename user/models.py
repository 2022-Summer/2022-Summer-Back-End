from django.db import models


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'headshot.' + ext
    return 'headshot/user_{0}/{1}'.format(instance.id, filename)


class User(models.Model):
    mailbox = models.EmailField(unique=True, default='', primary_key=True)
    username = models.CharField(max_length=20)
    real_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20, default='')
    description = models.CharField(max_length=255, default='')
    sex = models.CharField(max_length=5, default='')
    headshot = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def photo_url(self):
        if self.headshot and hasattr(self.headshot, 'url'):
            return 'http://127.0.0.1:8000'+ self.headshot.url
        else:
            return 'http://127.0.0.1:8000/media/default/user.jpeg'
