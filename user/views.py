from team.models import Invitation, Membership
from user.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == 'POST':
        mailbox = request.POST.get('mailbox')
        username = request.POST.get('username')
        real_name = request.POST.get('name')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        users = User.objects.filter(mailbox=mailbox)
        if users.exists():
            return JsonResponse({'errno': 1002, 'msg': "该已注册"})
        if password_1 != password_2:
            return JsonResponse({'errno': 1003, 'msg': "两次输入的密码不一致"})
        if request.session.get('verification_code', 0) != request.POST.get('code'):
            return JsonResponse({'errno': 1004, 'msg': "验证码错误"})
        User.objects.create(mailbox=mailbox, username=username, real_name=real_name, password=password_1)
        return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        mailbox = request.GET.get('mailbox')
        print(mailbox)
        users = User.objects.filter(mailbox=mailbox)
        if users.exists():
            return JsonResponse({'errno': 1002, 'msg': "该已注册"})
        try:
            rand_str = sendMessage(mailbox)  # 发送邮件
            request.session['verification_code'] = rand_str  # 验证码存入session，用于做注册验证
        except:
            return JsonResponse({'errno': 1003, 'msg': "发送验证码失败"})
        return JsonResponse({'errno': 0, 'msg': "发送验证码成功"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        mailbox = request.POST.get('mailbox')
        password = request.POST.get('password')
        if User.objects.filter(mailbox=mailbox).exists():
            user = User.objects.get(mailbox=mailbox)
            if user.password == password:
                request.session['mailbox'] = mailbox
                request.session['username'] = user.username
                return JsonResponse({'errno': 0, 'msg': "登录成功", 'username': user.username, 'mailbox': mailbox})
            else:
                return JsonResponse({'errno': 2002, 'msg': "密码错误"})
        else:
            return JsonResponse({'errno': 2003, 'msg': "用户不存在"})
        pass
    else:
        return JsonResponse({'errno': 2001, 'msg': "请求方式错误"})


@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'errno': 0, 'msg': "注销成功"})


@csrf_exempt
def sendMessage(mailbox):
    import random
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
    message = "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
    print(rand_str)
    mailBoxes = []
    mailBoxes.append(mailbox)
    send_mail('墨书验证码', message, '1030519668@qq.com', mailBoxes, fail_silently=False)
    return rand_str


@csrf_exempt
def password(request):
    if request.method == 'POST':
        mailbox = request.POST.get('mailbox')
        if User.objects.filter(mailbox=mailbox).exists():
            if request.session.get('verification_code', 0) == request.POST.get('code'):
                return JsonResponse({'errno': 0, 'password': User.objects.get(mailbox=mailbox).password})
            else:
                return JsonResponse({'errno': 4002, 'msg': "验证码错误"})
        else:
            return JsonResponse({'errno': 4003, 'msg': "用户不存在"})
    else:
        mailbox = request.GET.get('mailbox')
        try:
            rand_str = sendMessage(mailbox)  # 发送邮件
            request.session['verification_code'] = rand_str  # 验证码存入session，用于做注册验证
        except:
            return JsonResponse({'errno': 1003, 'msg': "发送验证码失败"})
        return JsonResponse({'errno': 0, 'msg': "发送验证码成功"})


@csrf_exempt
def info(request):
    mailbox = request.session.get('mailbox', '')
    if mailbox == '':
        return JsonResponse({'errno': 3001, 'msg': "用户未登录"})
    user = User.objects.get(mailbox=mailbox)
    if request.method == 'POST':
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('description'):
            user.description = request.POST.get('description')
        if request.POST.get('name'):
            user.real_name = request.POST.get('name')
        if request.POST.get('sex'):
            user.sex = request.POST.get('sex')
        if request.FILES.get('headshot'):
            user.headshot = request.FILES.get('headshot')
        if request.POST.get('password'):
            user.password = request.POST.get('password')
        user.save()
        return JsonResponse({'errno': 0, 'msg': "更改个人信息成功"})
    else:
        data = {
            'mailbox': user.mailbox,
            'username': user.username,
            'name': user.real_name,
            'description': user.description,
            'sex': user.sex,
            'password': user.password,
            'headshot': user.photo_url()
        }
        return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def invited_num(request):
    if request.method == 'GET':
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        invited_num = Invitation.objects.filter(user=user).count()
        invitations = [{
            'id': x.id,
            'teamID': x.team_id,
            'invitor': x.invitor.username,
            'inviteTime': x.invited_time.strftime("%Y-%m-%d %H:%M:%S"),
        } for x in Invitation.objects.filter(user=user)]
        return JsonResponse({'errno': 0, 'invitednum': invited_num, 'myInvitations': invitations})
    elif request.method == 'POST':
        invitation_id = request.POST.get('id', 0)
        op = int(request.POST.get('op', 0))
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        invitation = Invitation.objects.get(id=invitation_id)
        if op == 0:
            membership = Membership()
            membership.team = invitation.team
            membership.status = "普通用户"
            membership.user = user
            membership.save()
        invitation.delete()
        return JsonResponse({'errno': 0, 'msg': "处理邀请成功"})


@csrf_exempt
def team_info(request):
    if request.method == 'GET':
        mailbox = request.session.get('mailbox', '')
        user = User.objects.get(mailbox=mailbox)
        teams = [{
            'teamid': x.team.id,
            'name': x.team.name,
            'belong': Membership.objects.get(team=x.team, status='发起人').user.username,
            'foundedTime': x.team.founded_time,
        } for x in Membership.objects.filter(user=user)]
        return JsonResponse({'errno': 0, 'myTeams': teams})
