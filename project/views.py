import os
from shutil import copy

import pdfkit
import html2markdown
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

from project.models import Word, Document, Axure
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
        project = Project.objects.create(team=team, title=title, description=description, leader=user)
        word1 = Word()
        word1.last_editor = user
        word1.title = "答题模板"
        word1.project = project
        word1.html = """
            <h2><strong>2022 软件工程基础实验期末作业 答题模板</strong></h2><p><br></p><table style="width: 100%;"><tbody><tr><td colSpan="1" rowSpan="1" width="30">学号</td><td colSpan="1" rowSpan="1" width="295"></td></tr><tr><td colSpan="1" rowSpan="1" width="94">姓名</td><td colSpan="1" rowSpan="1" width="295"></td></tr><tr><td colSpan="1" rowSpan="1" width="94">班级</td><td colSpan="1" rowSpan="1" width="295"></td></tr></tbody></table><p><br></p><table style="width: 100%;"><tbody><tr><th colSpan="1" rowSpan="1" width="811">1. 请绘制Switch卡带租赁商店的用例图。</th></tr><tr><td colSpan="1" rowSpan="1" width="811">（请将用例图粘贴到下方）</td></tr><tr><td colSpan="1" rowSpan="1" width="811">（文字分析，不超过400字）<br><br><br><br><br><br><br><br><br></td></tr></tbody></table><p><br></p>
        """
        word1.save()
        word2 = Word()
        word2.last_editor = user
        word2.title = "通知模板"
        word2.project = project
        word2.html = """
            <h2 style="text-align: center;">关于开展2021-2022学年春季学期向党推优工作的通知</h2><p><br></p><p style="text-align: left;"><span style="font-family: 仿宋;">各学院（书院）分团委：</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">推荐优秀共青团员作党的发展对象（以下简称“推优”）是党赋予共青团组织的一项光荣任务，是基层团组织的一项基本任务。为加强和促进我校学生党员的发展工作，充分发挥我校先进基层团组织和优秀青年团员的模范先锋作用，进一步巩固和扩大党的执政的青年群众基础，现开展2021-2022学年春季学期向党推优工作，通知如下。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 黑体;">一、推优对象</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">全体本科生及研究生。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 黑体;">二、推优步骤</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">本科生和研究生向党推优工作按照双线并行、统一标准的原则，坚持民主集中制，严格遵照《共青团北京航空航天大学委员会推荐优秀团员作为党的发展对象工作细则（试行）》（附件一）完成推优工作。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">各学院（书院）分团委依据《2021-2022学年春学期“向党推优”注意事项及材料要求》（附件二），认真填写《团支部“向党推优”会议记录表》（附件三）、《“向党推优”登记表》（附件四）、《“向党推优”汇总表》（附件五），以学院（书院）为单位，提交至校（研）团委。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">校（研）团委组织部对材料进行审核、盖章，审批合格后留存一份《“向党推优”汇总表》，其余材料返回至各学院（书院）分团委，完成推优工作。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 黑体;">三、材料提交</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">本科生和研究生材料需分开提交，各学院（书院）分团委应于</span><span style="font-family: 仿宋;"><strong>4月15日17:00前</strong></span><span style="font-family: 仿宋;">将</span><span style="font-family: 仿宋;"><strong>本科生</strong></span><span style="font-family: 仿宋;">纸质版材料送至学院路校区知行北楼103室，电子版汇总表（附件五）发送至buaa_youth@163.com；</span><span style="font-family: 仿宋;"><strong>研究生</strong></span><span style="font-family: 仿宋;">纸质版材料与各系负责人联系报送，电子版汇总表（附件五）发送至各负责人邮箱。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">各学院（书院）分团委须严格审核，确保材料准确、规范。填写、提交材料前请认真阅读附件二，材料不符合要求者将取消相应团支部或团员本学期“推优”资格。</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">本科生联系人：李若婉 &nbsp; 15810726049</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;李裴林 &nbsp; 13755162186</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">办公电话：010-82339610</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">联系邮箱：buaa_youth@163.com</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">材料报送地址：学院路校区知行北楼103 室</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;"> </span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">研究生联系人：</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">01-08系：宗麒梦，13455320102，13455320102@163.com</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">09-17系：赵 &nbsp;萌，17320055823，zzhao_meng@163.com</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">19-28系：李泽宇，13121271215，1137310241@qq.com</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">29-43系：韩 &nbsp;曦，18613871855，hanxi19981231@buaa.edu.cn</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">附件：</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">1.《共青团北京航空航天大学委员会推荐优秀团员作为党的发展对象工作细则（试行）》</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">2.《2021-2022学年春季学期“向党推优”注意事项及材料要求》</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">3.《团支部“向党推优”会议记录表》</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">4.《“向党推优”登记表》</span></p><p style="text-indent: 32pt; text-align: left;"><span style="font-family: 仿宋;">5.《“向党推优”汇总表》</span></p><p><span style="font-family: 仿宋;"> </span></p><p style="text-indent: 32pt; text-align: right;"><span style="font-family: 仿宋;">共青团北京航空航天大学委员会</span></p><p style="text-indent: 32pt; text-align: right;"><span style="font-family: 仿宋;">2022年3月29日</span></p><table style="width: 100%;"><tbody><tr><td colSpan="1" rowSpan="1" width="692"><span style="font-family: 仿宋;">共青团北京航空航天大学委员会 2022年3月29日印发</span></td></tr></tbody></table><p style="text-align: left;"><br></p><p><br></p>
        """
        word2.save()
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
            new_file_path = 'resource/team_{0}/project_{1}/{2}'.format(new_doc.project.team.id, new_project.id,
                                                                       doc.file.name.split('/')[-1])
            copy(str(doc.file), new_file_path)
            new_doc.file = new_file_path
            new_doc.save()

        return JsonResponse({'errno': 0, 'msg': "复制成功"})


@csrf_exempt
def download_word(request):
    if request.method == 'GET':
        word_id = int(request.GET.get('wordid', 0))
        word = Word.objects.get(id=word_id)
        filetype = int(request.GET.get('type', 0))
        for i in os.listdir('resource/tmp'):
            os.remove('resource/tmp/' + i)
        if filetype == 1:
            # path_wk = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
            # config = pdfkit.configuration(wkhtmltopdf=path_wk)
            options = {
                'page-size': 'A4',
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
            pdfkit.from_string(word.html, 'resource/tmp/' + str(word.title) + '.pdf', options=options,)
            return FileResponse(open('resource/tmp/' + str(word.title) + '.pdf', 'rb'), as_attachment=True)
        elif filetype == 2:
            markdown = html2markdown.convert(word.html)
            with open('resource/tmp/' + str(word.title) + '.md', 'w', encoding='utf-8') as file:
                file.write(markdown)
            return FileResponse(open('resource/tmp/' + str(word.title) + '.md', 'rb'), as_attachment=True)


@csrf_exempt
def axure_info(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        axures = [{
            'id': x.id,
            'title': x.title,
            'lastEditTime': x.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"),
        } for x in Axure.objects.filter(project=project)]
        return JsonResponse({'errno': 0, 'msg': "查询成功", 'file': axures})


@csrf_exempt
def view_axure(request):
    if request.method == 'POST':
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        axure_id = int(request.POST.get('axureID', 0))
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        if axure_id == 0:
            axure = Axure()
            axure.last_editor = user
            axure.project = project
            axure.save()
        else:
            axure = Axure.objects.get(id=axure_id)
        return JsonResponse({'errno': 0, 'msg': "查询成功", 'axureID': axure.id, 'axureContent': axure.content})


@csrf_exempt
def save_axure(request):
    if request.method == 'POST':
        try:
            mailbox = request.session.get('mailbox', '')
            user = User.objects.get(mailbox=mailbox)
            axure_id = request.POST.get('axureID', 0)
            axure = Axure.objects.get(id=axure_id)
            axure.title = request.POST.get('axurename')
            axure.content = request.POST.get('axureData')
            axure.last_editor = user
            axure.save()
            return JsonResponse({'errno': 0, 'msg': "保存成功"})
        except:
            return JsonResponse({'errno': 11001, 'msg': "保存失败"})


@csrf_exempt
def delete_axure(request):
    if request.method == 'POST':
        axure_id = request.POST.get('id', 0)
        try:
            axure = Axure.objects.get(id=axure_id)
            axure.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})
        except:
            return JsonResponse({'errno': 12001, 'msg': "删除失败"})


@csrf_exempt
def preview_axure(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        axure_id = request.POST.get('axureid', 0)
        print(axure_id)
        axure = Axure.objects.get(id=axure_id)
        if axure.preview:
            return JsonResponse({'errno': 0, 'msg': "预览成功", 'axureContent': axure.content})
        else:
            return JsonResponse({'errno': 1, 'msg': "该项目未开启预览"})


@csrf_exempt
def change_preview(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        op = int(request.POST.get('op', 0))
        project = Project.objects.get(id=project_id)
        if op == 0:
            for x in Axure.objects.filter(project=project):
                x.preview = True
                x.save()
        elif op == 1:
            for x in Axure.objects.filter(project=project):
                x.preview = False
                x.save()
        return JsonResponse({'errno': 0, 'msg': "更改成功"})


@csrf_exempt
def preview_state(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectid')
        project = Project.objects.get(id=project_id)
        axure = Axure.objects.filter(project=project)
    for x in axure:
        state = x.preview
    return JsonResponse({'errno': 0, 'state': state})


@csrf_exempt
def preview_info(request):
    if request.method == 'POST':
        project_id = request.POST.get('projectid', 0)
        project = Project.objects.get(id=project_id)
        prototypes = [{
            'axureid': x.id,
            'label': x.title,
        } for x in Axure.objects.filter(project=project)]
        return JsonResponse({'errno': 0, 'msg': "获取成功", 'prototypes': prototypes})
