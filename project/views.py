from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from project.models import Word, Document, project_directory_path
from team.models import Team, Project
from user.models import User


@csrf_exempt
def new_project(request):
    if request.method == 'POST':
        team_id = request.POST.get('teamid', 0)
        mailbox = request.session.get('mailbox', 0)
        team = Team.objects.get(id=team_id)
        user = User.objects.get(mailbox=mailbox)
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        Project.objects.create(team=team, title=title, description=description, leader=user)
        return JsonResponse({'errno': 0, 'msg': "创建项目成功"})


@csrf_exempt
def word(request):
    if request.method == 'GET':
        word_id = request.GET.get('wordid', 0)
        if word_id == 0:
            project_id = request.GET.get('projectid', 0)
            project = Project.objects.get(id=project_id)
            word = Word()
            word.project = project
            word.save()
        else:
            word = Word.objects.get(id=word_id)
        return JsonResponse({'errno': 0, 'wordid': word.id, 'html': word.html})
    elif request.method == 'POST':
        word_id = request.POST.get('wordid', 0)
        word = Word.objects.get(id=word_id)
        title = request.POST.get('title', '')
        html = request.POST.get('html', '')
        if title != '':
            word.title = title
        if html != '':
            word.html = html
        word.save()
        return JsonResponse({'errno': 0, 'msg': "保存成功"})


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        type = request.POST.get('type', 0)
        doc = Document()
        doc.title = request.POST.get('title', '')
        doc.type = type
        doc.project = project
        doc.uploader = user
        doc.file = request.FILES.get('file')
        doc.save()
        return JsonResponse({'errno': 0, 'msg': "上传成功"})


@csrf_exempt
def download(request):
    if request.method == 'GET':
        doc_id = request.GET.get('fileid', '')
        doc = Document.objects.get(id=doc_id)
        return FileResponse(open(str(doc.file), 'rb'), as_attachment=True)


@csrf_exempt
def real_name(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        new_name = request.POST.get('newname', '')
        print(project_id)
        project = Project.objects.get(id=project_id)
        if new_name:
            project.title = new_name
            project.save()
        return JsonResponse({'errno': 0, 'msg': "重命名成功"})


def file_info(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        type = request.POST.get('type', 0)
        file = [{
            'id': x.id,
            'title': x.title,
            'lastEditTime': x.uploaded_time
        } for x in Document.objects.filter(project=project, type=type)]
        return JsonResponse({'errno': 0, 'msg': "查询文件信息成功", 'file': file})


@csrf_exempt
def doc(request):
    if request.method == 'GET':
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        word = [{
            'id': x.id,
            'title': x.title,
            'lastEditor': x.last_editor.username,
            'lastEditTime': x.last_edit_time,
        } for x in Word.objects.filter(project=project)]
        return JsonResponse({'errno': 0, 'msg': "查询文档信息成功", 'word': word})