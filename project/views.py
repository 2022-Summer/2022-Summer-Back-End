import pdfkit
import html2markdown
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
        word_id = int(request.GET.get('wordid', 0))
        print(word_id)
        if word_id == 0:
            project_id = request.GET.get('projectid', 0)
            project = Project.objects.get(id=project_id)
            word = Word()
            word.project = project

            word.last_editor = User.objects.get(mailbox=request.session.get("mailbox"))
            word.save()
        else:
            word = Word.objects.get(id=word_id)
            word.last_editor = User.objects.get(mailbox=request.session.get("mailbox"))
            word.save()
        return JsonResponse({'errno': 0, 'wordid': word.id, 'title': word.title, 'html': word.html})
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
        if Document.objects.filter(title=file.name).exists():
            doc = Document.objects.get(title=file.name)
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
def downloadword(request):
    if request.method == 'GET':
        word_id = int(request.GET.get('wordid', 0))
        word = Word.objects.get(id=word_id)
        filetype = int(request.GET.get('type', 0))
        if filetype == 1:
            path_wk = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
            config = pdfkit.configuration(wkhtmltopdf=path_wk)
            options = {
                'page-size': 'A4',
                'header-html': 'http://localhost:8080/static/data/pdfHeader.html',
                # 设置页眉数据，作为页眉的html页面必须有<!DOCTYPE html>
                'header-spacing': '3',  # 设置页眉与正文之间的距离，单位是毫米
                'header-right': 'Quality Report',  # 设置页眉右侧数据
                'header-font-size': 10,  # 设置页眉字体大小
                'footer-font-size': 10,  # 设置页脚字体大小
                'footer-right': '[page]/[topage]',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.5in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                # 'no-outline': None, #为None时表示确定，则不生成目录
                'header-line': None,  # 为None时表示确定，生成页眉下的线
            }
            pdfkit.from_string(word.html, './test.pdf', options=options, configuration=config)
            return FileResponse(open('./test.pdf', 'rb'), as_attachment=True)
        elif filetype == 2:
            markdown = html2markdown.convert(word.html)
            with open('test.md', 'w', encoding='utf-8') as file:
                file.write(markdown)
            return FileResponse(open('./test.md', 'rb'), as_attachment=True)


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
            'lastEditTime': x.uploaded_time.strftime("%Y-%m-%d %H:%M:%S")
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
