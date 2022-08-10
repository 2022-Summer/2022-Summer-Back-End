from django.urls import path

from project.views import *

urlpatterns = [
    path('new/', new_project),
    path('word/', word),
    path('upload/', upload),
    path('download/', download),
    path('rename/', re_name),
    path('file/', file_info),
    path('doc/', doc),
    path('delete/', delete_doc),
    path('deword/', delete_word),
    path('copy/', copy_project),
    path('downloadword/', download_word),
    path('view/', axure_info),
    path('viewaxure/', view_axure),
    path('axuresave/', save_axure),
    path('deleteaxure/', delete_axure),
    path('preview/', preview_axure),
    path('change/', change_preview),
]