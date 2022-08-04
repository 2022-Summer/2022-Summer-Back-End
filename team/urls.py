from django.urls import path

from team.views import *

urlpatterns = [
    path('message/', team_info),
    path('member/', member_info),
    path('found/', found),
    path('invite/', invite),
    path('admin/', admin),
    path('project/', project),
    path('recycle/', recycle),
]