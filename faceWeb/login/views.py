from django.http import HttpResponse
from django.shortcuts import render
from register import models

from camera.views import camera, camera2


def facelogin(request):
    if request.method == 'POST':
        name = camera2()
        if name == False:
            return HttpResponse("人脸认证失败")
        else:
            return HttpResponse("你好!{}，已登录。".format(name))
    else:
        return render(request, 'camera.html')

def tologin(request):
    if request.method == "POST":
        username = request.POST.get('usernameOrEmail', None)
        password = request.POST.get('password', None)
        faceValue = camera(username)
        if username and password and faceValue:  # 确保用户名和密码都不为空
            try:
                user = models.userdata.objects.get(username=username)
            except:
                user = models.userdata.objects.get(email=username)
            if user.password == password:
                return render(request, 'login.html')
            else:
                return render(request, 'failed.html')
        else:
            return HttpResponse("人脸认证失败")
    else:
        return render(request, 'logout.html')


def login(request):
    return render(request, 'login.html')