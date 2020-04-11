from django.shortcuts import render
from .models import Name_Picture
from django.http import HttpResponse, HttpResponseRedirect
import os
import redis
import random

red = redis.Redis(host='localhost', port=6379, db=1)


def data(request):
    datas = Name_Picture.get_all()

    context = {
        'datas': datas,
    }
    return render(request, 'data.html', context=context)


def index(request):
    return render(request, 'index.html')


def upload_file(request):

    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join('facePhoto', myFile.name), 'wb+')    # 打开特定的文件进行二进制的写操作

        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        pictureLocation = os.path.join('facePhoto', myFile.name)
        data = Name_Picture()
        data.picture = pictureLocation
        username = request.POST['username']
        data.names = username
        data.save()

        red.set(username, pictureLocation)

        return HttpResponseRedirect('/index/')

    elif request.method == 'GET':
        return render(request, 'index.html')


def chouqian(request):
    red = redis.StrictRedis(host='localhost', port=6379, db=1)
    facesName = red.keys()
    facesName = list(set(facesName))
    facesResult = random.sample(facesName, 2)
    facesResult2 = []
    for face in facesResult:
        facesResult2.append(str(face, 'utf-8'))

    routes = []
    for face in facesResult:
        routes.append(red.get(face).decode('utf-8'))

    result = dict(zip(facesResult2, routes))

    courses = [
        '声速测量',
        '粘度系数测定',
        '单缝衍射实验',
        '霍尔效应',
        '电子示波器实验',
        '测薄透镜焦距',
        '迈克尔逊干涉实验',
        '牛顿环和劈尖干涉',
        '分光计测折射率',
        '磁滞回线的测定',
    ]
    course = random.sample(courses, 2)

    context = {
        'result': result,
        'course': course,
    }
    return render(request, 'chouqian.html', context=context)


def course(request):
    courses = [
        '声速测量',
        '粘度系数测定',
        '单缝衍射实验',
        '霍尔效应',
        '电子示波器实验',
        '测薄透镜焦距',
        '迈克尔逊干涉实验',
        '牛顿环和劈尖干涉',
        '分光计测折射率',
        '磁滞回线的测定',
    ]
    Course = random.sample(courses, 1)
    context = {
        'Course': Course,
    }
    return render(request, 'chouqian.html', context=context)