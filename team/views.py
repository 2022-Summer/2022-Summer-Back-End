from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from project.models import Word
from team.models import Team, Membership, Project, Invitation
from user.models import User


@csrf_exempt
def team_info(request):
    if request.method == 'GET':
        team_id = request.GET.get('teamid', 0)
        team = Team.objects.get(id=team_id)
        data = {
            'teamname': team.name,
            'belong': Membership.objects.get(team=team, status="发起人").user.username,
            'foundedtime': team.founded_time.strftime("%Y-%m-%d %H:%M:%S"),
            'memberNum': team.members.all().count(),
            'intro': team.intro,
        }
        return JsonResponse({'errno': 0, 'msg': "获取团队信息成功", 'data': data})


@csrf_exempt
def member_info(request):
    if request.method == 'GET':
        team_id = request.GET.get('teamid', 0)
        team = Team.objects.get(id=team_id)
        print(team.members.all())
        members = [{
            'name': x.real_name,
            'username': x.username,
            'email': x.mailbox,
            'status': Membership.objects.get(team=team, user=x).status,
            'description': x.description,
            'sex': x.sex,
        } for x in team.members.all()]
        mailbox = request.session.get('mailbox', 0)
        user = User.objects.get(mailbox=mailbox)
        return JsonResponse({'errno': 0, 'msg': "获取成员信息成功",
                             'MyStatus': Membership.objects.get(team=team, user=user).status,
                             'Members': members})


@csrf_exempt
def found(request):
    if request.method == 'POST':
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        team = Team()
        team.name = request.POST.get('teamname')
        team.intro = request.POST.get('intro', '')
        team.save()
        membership = Membership(user=user, team=team, status='发起人')
        membership.save()
        return JsonResponse({'errno': 0, 'msg': "创建团队成功"})


@csrf_exempt
def invite(request):
    if request.method == 'POST':
        team_id = request.POST.get('teamid', 0)
        mailbox = request.POST.get('email', '')
        op = int(request.POST.get('op', 0))
        if not User.objects.filter(mailbox=mailbox).exists():
            return JsonResponse({'errno': 8001, 'msg': "该成员不存在"})
        user = User.objects.get(mailbox=mailbox)
        mailbox = request.session.get('mailbox', '')
        invitor = User.objects.get(mailbox=mailbox)
        team = Team.objects.get(id=team_id)
        if op == 0:
            if user in team.members.all():
                return JsonResponse({'errno': 8002, ',msg': "该成员已在团队中"})
            else:
                invitation = Invitation()
                invitation.user = user
                invitation.team = team
                invitation.invitor = invitor
                invitation.save()
            return JsonResponse({'errno': 0, 'msg': "已发送邀请"})
        elif op == 1:
            membership = Membership.objects.get(team=team, user=user)
            if membership.status == '发起人':
                team.delete()
            else:
                membership.delete()
            return JsonResponse({'errno': 0, 'msg': "已成功移除"})
    else:
        return JsonResponse({'errno': 8003, ',msg': "请求方式错误"})


@csrf_exempt
def admin(request):
    if request.method == 'POST':
        op = int(request.POST.get('op', 0))
        mailbox = request.POST.get('email', '')
        team_id = request.POST.get('teamid', 0)
        user = User.objects.get(mailbox=mailbox)
        team = Team.objects.get(id=team_id)
        membership = Membership.objects.get(team=team, user=user)
        if op == 0:
            membership.status = '管理员'
        elif op == 1:
            membership.status = '普通用户'
        membership.save()
        return JsonResponse({'errno': 0, 'msg': "更改成功"})


@csrf_exempt
def project(request):
    if request.method == 'POST':
        pass
    else:
        team_id = request.GET.get('teamid', 0)
        team = Team.objects.get(id=team_id)
        projects = [{
            'id': x.id,
            'title': x.title,
            'startTime': x.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'leader': x.leader.username,
            'description': x.description,
        } for x in Project.objects.filter(team=team, recycled=False).order_by('-start_time')]
        return JsonResponse({'errno': 0, 'msg': "获取项目信息成功", 'projects': projects})


@csrf_exempt
def recycle(request):
    if request.method == 'POST':
        team_id = request.POST.get('teamid', 0)
        project_id = request.POST.get('projectid', 0)
        team = Team.objects.get(id=team_id)
        project = Project.objects.get(id=project_id)
        op = int(request.POST.get('op', 0))
        if op == 0:
            project.recycled = True
            project.save()
        elif op == 1:
            project.recycled = False
            project.save()
        else:
            project.delete()
        return JsonResponse({'errno': 0, 'msg': "操作成功"})
    else:
        team_id = request.GET.get('teamid')
        team = Team.objects.get(id=team_id)
        recycles = [{
            'title': x.title,
            'startTime': x.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'leader': x.leader.username,
            'id': x.id,
        } for x in Project.objects.filter(team=team, recycled=True)]
        return JsonResponse({'errno': 0, 'msg': "获取项目信息成功", 'Recycle': recycles})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        team_id = request.POST.get('teamid', 0)
        keyword = request.POST.get('keyword', '')
        team = Team.objects.get(id=team_id)
        print(keyword)
        projects = [{
            'id': x.id,
            'title': x.title,
            'startTime': x.start_time,
            'leader': x.leader.username,
        } for x in Project.objects.filter(Q(team=team), Q(title__icontains=keyword) |
                                          Q(leader__username__icontains=keyword) |
                                          Q(description__icontains=keyword))]
        return JsonResponse({'errno': 0, 'msg': "搜索成功", 'projects': projects})


@csrf_exempt
def get_word(request):
    if request.method == 'GET':
        team_id = request.GET.get('teamid', 0)
        team = Team.objects.get(id=team_id)
        projects = [{
            'projectid': x.id,
            'label': x.title,
            'children': [{
                'wordid': y.id,
                'label': y.title,
                'lastEditor': y.last_editor.username,
                'lastEditTime': y.last_edit_time.strftime("%Y-%m-%d %H:%M:%S"),
            } for y in Word.objects.filter(project=x)]
        } for x in Project.objects.filter(team=team)]
        return JsonResponse({'errno': 0, 'msg': "获取文档信息成功", 'Files': projects})
