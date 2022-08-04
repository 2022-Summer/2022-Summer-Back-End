from django.urls import path
from user.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('password/', password),
    path('info/', info),
    path('invited/', invited_num),
    path('team/', team_info),
]