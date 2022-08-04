from django.urls import path

from project.views import *

urlpatterns = [
    path('new/', new_project),
    path('word/', word),
    path('upload/', upload),
    path('download/', download),
]