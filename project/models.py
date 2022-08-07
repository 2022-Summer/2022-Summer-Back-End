from django.utils import timezone

from django.db import models

from team.models import Project
from user.models import User


def project_directory_path(instance, filename):
    return 'resource/team_{0}/project_{1}/{2}'.format(instance.project.team.id, instance.project_id, filename)


class Word(models.Model):
    title = models.CharField(max_length=20)
    html = models.TextField(default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_editor = models.ForeignKey(User, on_delete=models.CASCADE)
    last_edit_time = models.DateTimeField('修改时间',default = timezone.now)


class Document(models.Model):
    title = models.CharField(max_length=100, unique=True)
    type = models.BooleanField()
    file = models.FileField(upload_to=project_directory_path, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_time = models.DateTimeField('保存时间',default = timezone.now)
