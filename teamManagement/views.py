from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        real_name = request.POST.get('name')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        users = User.objects.filter(email=email)
        if users.exists():
            return JsonResponse({'errno': 1002, 'msg': "该学号已注册"})
        if password_1 != password_2:
            return JsonResponse({'errno': 1003, 'msg': "两次输入的密码不一致"})

        User.objects.create(email=email, username=username, real_name=real_name, password=password_1)
        return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.password == password:
                request.session['email'] = email
                request.session['username'] = user.username
                if user.first_login:
                    user.first_login = False
                return JsonResponse({'errno': 0, 'msg': "登录成功", 'username': user.username})
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
def sendMessage(email):
    import random
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
    message = "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
    print(rand_str)
    emailBox = []
    emailBox.append(email)
    send_mail('墨书验证码', message, '1030519668@qq.com', emailBox, fail_silently=False)
    return rand_str


def existUser(email):
    created = 1
    try:
        User.objects.get(email=email)
    except:
        created = 0
    return created


@csrf_exempt
def send_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if existUser(email):
            JsonResponse({'errno': 3002, 'msg': "用户已注册"})
        else:
            try:
                rand_str = sendMessage(email)  # 发送邮件
                request.session['verification_code'] = rand_str  # 验证码存入session，用于做注册验证
            except:
                return JsonResponse({'errno': 3002, 'msg': "发送验证码失败"})
        return JsonResponse({'errno': 0, 'msg': "发送验证码成功"})
    else:
        return JsonResponse({'errno': 3001, 'msg': "请求方式错误"})
