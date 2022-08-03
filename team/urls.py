from django.urls import path

from team.views import *

urlpatterns = [
    path('message/', team_info),
    path('member/', member_info),
    path('create/', create),
]