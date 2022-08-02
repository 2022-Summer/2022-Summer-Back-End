from django.urls import path
from teamManagement.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
]