from django.db import models

from user.models import User


class Team(models.Model):
    name = models.CharField(max_length=20, default='')
    founded_time = models.DateTimeField(auto_now_add=True)
    intro = models.CharField(max_length=255, default='')
    members = models.ManyToManyField(User, through='Membership')


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(max_length=5)


class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    start_time = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default='')
    recycled = models.BooleanField(default=False)


class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    invitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitor')
    invited_time = models.DateTimeField(auto_now_add=True)
