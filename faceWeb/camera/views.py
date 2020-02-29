import cv2
import pyttsx3
import face_recognition
import numpy as np
import redis
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def camera(request):
    face_cascade = cv2.CascadeClassifier(
        "C:\\Users\\TIM\\cascades\\haarcascade_frontalface_default.xml")
    red = redis.StrictRedis(host='localhost', port=6379, db=1)

    keys = red.keys()
    for key in keys:
        image = face_recognition.load_image_file(red.get(key))
        face_encoding = face_recognition.face_encodings(image)[0]
        namelist = []
        namelist.append(key)

        camera = cv2.VideoCapture(0)
        while True:
            # 参数ret 为True 或者False,代表有没有读取到图片
            # 第二个参数frame表示截取到一帧的图片
            ret, frame = camera.read()
            # frame = cv2.imread(r'C:\Users\TIM\c.jpg')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.5, 3)
            for (x, y, w, h) in face:
                # 绘制矩形框，颜色值的顺序为BGR，即矩形的颜色为蓝色
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

            cv2.imshow('camera', frame)

            k = cv2.waitKey(1)
            if k == ord('s'):
                rgb_frame = frame[:, :, ::-1]

                # 获取画面中的所有人脸位置及人脸特征码

                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # 对获取的每个人脸进行识别比对
                for (top, right, bottom, left), face_encodings in list(zip(face_locations, face_encodings)):
                    print(face_encodings)
                    print(face_encodings.shape)
                    # 对其中一个人脸的比对结果（可能比对中人脸库中多个人脸）
                    print(np.array(face_encoding.shape))
                    print([np.array(face_encoding)])
                    matches = face_recognition.compare_faces(
                        [np.array(list(face_encoding))], face_encodings, tolerance=0.47)
                    # 默认只认为是比对中的第一个人脸.
                    print(matches)
                if True in matches:
                    first_match_index = matches.index(True)
                    engine = pyttsx3.init()
                    engine.say('你好,{}'.format(namelist[first_match_index].decode('utf-8')))
                    engine.runAndWait()
                else:
                    engine = pyttsx3.init()
                    engine.say('识别失败或者不在库内')
                    engine.runAndWait()
            if k == ord('q'):
                break

        camera.release()
        return render(request, 'home.html')

