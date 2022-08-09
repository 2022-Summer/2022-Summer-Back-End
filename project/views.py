import os
from shutil import copy

from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from html2text import html2text

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
        word_id = int(request.GET.get('wordid', 0))
        if word_id == 0:
            project_id = request.GET.get('projectid', 0)
            project = Project.objects.get(id=project_id)
            mailbox = request.session.get('mailbox', '')
            user = User.objects.get(mailbox=mailbox)
            word = Word()
            word.last_editor = user
            word.project = project
            word.save()
        else:
            mailbox = request.session.get('mailbox', '')
            user = User.objects.get(mailbox=mailbox)
            word = Word.objects.get(id=word_id)
            word.last_editor = user
            word.save()
        return JsonResponse({'errno': 0, 'wordid': word.id, 'title': word.title,'html': word.html})
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

        file = request.FILES.get('file')
        if Document.objects.filter(title=file.name, project=project).exists():
            doc = Document.objects.get(title=file.name, project=project)
            doc.file.delete()
            doc.file = file
            doc.save()
        else:
            doc = Document()
            doc.title = file.name
            doc.type = type
            doc.project = project
            doc.uploader = user
            doc.file = file
            doc.save()
        return JsonResponse({'errno': 0, 'msg': "上传成功"})


@csrf_exempt
def download(request):
    if request.method == 'GET':
        doc_id = int(request.GET.get('fileid'))
        doc = Document.objects.get(id=doc_id)
        return FileResponse(open(str(doc.file), 'rb'), as_attachment=True)


@csrf_exempt
def re_name(request):
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
    if request.method == 'GET':
        project_id = request.GET.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        type = request.GET.get('type', 0)
        file = [{
            'id': x.id,
            'title': x.title,
            'lastEditTime': x.uploaded_time.strftime("%Y-%m-%d %H:%M:%S"),
        } for x in Document.objects.filter(project=project, type=type)]
        return JsonResponse({'errno': 0, 'msg': "查询文件信息成功", 'file': file})


@csrf_exempt
def doc(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        word = [{
            'id': x.id,
            'title': x.title,
            'lastEditor': x.last_editor.username,
            'lastEditTime': x.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"),
        } for x in Word.objects.filter(project=project)]
        return JsonResponse({'errno': 0, 'msg': "查询文档信息成功", 'word': word})


@csrf_exempt
def delete_doc(request):
    if request.method == 'POST':
        doc_id = request.POST.get('fileid', 0)
        doc = Document.objects.get(id=doc_id)
        doc.file.delete()
        doc.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})


@csrf_exempt
def delete_word(request):
    if request.method == 'POST':
        word_id = request.POST.get('wordid', 0)
        word = Word.objects.get(id=word_id)
        word.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功"})


@csrf_exempt
def copy_project(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        new_project = project
        new_project.pk = None
        new_project.save()
        for word in Word.objects.filter(project_id=project_id):
            new_word = word
            new_word.pk = None
            new_word.project = new_project
            new_word.save()
        for doc in Document.objects.filter(project_id=project_id):
            new_doc = Document()
            new_doc.title = doc.title
            new_doc.type = doc.type
            new_doc.project = new_project
            new_doc.uploader = doc.uploader
            new_doc.uploaded_time = doc.uploaded_time
            new_doc = doc
            new_doc.pk = None
            new_doc.project = new_project
            if not os.path.exists('resource/team_{0}/project_{1}'.format(new_doc.project.team.id, new_project.id)):
                os.mkdir('resource/team_{0}/project_{1}'.format(new_doc.project.team.id, new_project.id))
            new_file_path = 'resource/team_{0}/project_{1}/{2}'.format(new_doc.project.team.id, new_project.id, doc.file.name.split('/')[-1])
            copy(str(doc.file), new_file_path)
            new_doc.file = new_file_path
            new_doc.save()

        return JsonResponse({'errno': 0, 'msg': "复制成功"})


@csrf_exempt
def download_word(request):
    if request.method == 'GET':
        word_id = request.GET.get('wordid', 0)
        type = int(request.GET.get('type', 0))
        word = Word.objects.get(id=word_id)
        if type == 2:
            markdown = html2text(word.html)
            file = open(str(word.title) + '.md', 'w', encoding='utf-8')
            file.write(markdown)
            file.close()
            return FileResponse(open(str(word.title) + '.md', 'rb'), as_attachment=True)
