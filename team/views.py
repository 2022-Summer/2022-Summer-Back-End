from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from team.models import Team, Membership
from user.models import User


@csrf_exempt
def team_info(request):
    if request.method == 'GET':
        team_id = request.GET.get('teamid', 0)
        team = Team.objects.get(id=team_id)
        data = {
            'teamname': team.name,
            'belong': Membership.objects.get(team=team, status="发起人").user.username,
            'foundedtime': team.founded_time,
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
            'status': Membership.objects.get(team=team, user=x),
            'description': x.description,
        } for x in team.members.all()]
        mailbox = request.session.get('mailbox', 0)
        user = User.objects.get(mailbox=mailbox)
        return JsonResponse({'errno': 0, 'msg': "获取成员信息成功",
                             'MyStatus': Membership.objects.get(team=team, user=user).status,
                             'Members': members})


@csrf_exempt
def create(request):
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

