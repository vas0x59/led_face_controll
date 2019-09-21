from Device import Device
import Animations
import math
import time
import threading
from Utils import *

import cv2
import dlib
import face_recognition
import pickle
import glob
import numpy as np


dev = Device(led_count=4*4*2, servo_count=3, brightness=1, update_rate=30)
dev.connect()
dev.start()


################################################################
anim_rate = 70

l1 = Animations.Linear2_i_1(speed=15/anim_rate)
l2 = Animations.Linear_i_1(speed=50/anim_rate)

sin1 = Animations.Sin_n_i_1(speed=120/anim_rate)
sin_arr = Animations.Sin_arr_i_1(4*4*2, speed=5/anim_rate, k=5)

rgb_v1 = Animations.RGB_sin_v1_full_led(dev, speed=160/anim_rate)

anim_now = "none"


def anim():
    while True:
        if anim_now == "rgb_v1":
            rgb_v_leds = rgb_v1.tick()
            dev.leds = rgb_v_leds
        elif anim_now == "rg":
            l1_v = l1.tick()
            dev.set_color_all(((l1_v)*255, (1-l1_v)*255, 0))
        elif anim_now == "geor":
            l1_v = l1.tick()
            dev.set_color_all((255*0.7, 0, 255*0.3))
        elif anim_now == "rb":
            l1_v = l1.tick()
            dev.set_color_all(((l1_v)*255, 0, (1-l1_v)*255))
        elif anim_now == "none":
            dev.set_color_all((0, 0, 0))
        elif anim_now == "sin_r":
            sin_arr_v = sin_arr.tick()
            # print(sin_arr_v)
            dev.leds = [check_color((i*255, 0, 0)) for i in sin_arr_v]
        elif anim_now == "sin_g":
            sin_arr_v = sin_arr.tick()
            # print(sin_arr_v)
            dev.leds = [check_color((0, 255*i, 0)) for i in sin_arr_v]
        elif anim_now == "sin_b":
            sin_arr_v = sin_arr.tick()
            # print(sin_arr_v)
            dev.leds = [check_color((0, 255*i*0.2, 255*i*0.8)) for i in sin_arr_v]
        time.sleep(1/anim_rate)


anim_th = threading.Thread(target=anim)
anim_th.daemon = True
anim_th.start()

anim_now = "none"
################################################################


def crop_by_box(image, b, m=1.2):
    w = abs(b[1][0]-b[0][0])
    h = abs(b[1][1]-b[0][1])
    w *= m
    h *= m
    x = (b[1][0]+b[0][0]) / 2
    y = (b[1][1]+b[0][1]) / 2
    # cv2.circle(image, (int(x), int(y)), 10, (0, 0, 255))
    crop = image[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)]
    return crop
    # cv2.imshow(str(i) + "_hog", crop)
    # cv2.rectangle(out, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (0, 0, 255), 2)


def face_box_to_xyxy(b):
    (y1, x2, y2, x1) = b
    return ((x1, y1), (x2, y2))



encodings = []
ids_enc = []
for p_file in sorted(glob.glob('./faces' + '/*.pickle')):
    print(p_file)
    st_enc = pickle.load(open(p_file, 'rb'))
    encodings.append(st_enc[1])
    ids_enc.append(st_enc[0])

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

i = 0
resize_k = 0.7
################################################################

ln_count = 28
last_names = [[] for i in range(ln_count)]

def get_last_name(name_to_find):
    d_c = 0
    for fn in last_names:
        for name in fn:
            if name == name_to_find:
                d_c += 1
    print(d_c)
    if (d_c / ln_count) > 0.6:
        return True
    else:
        return False

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imshow("frame", frame)
    if i >= 2:
        i = 0
        resultImage = frame.copy()
        rgb = frame[:, :, ::-1]

        resized = cv2.resize(frame, (0, 0), fx=resize_k, fy=resize_k)
        cv2.imshow("resized", resized)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", gray)

        face_locations = faceCascade.detectMultiScale(gray, 1.3, 5)

        fl = []
        for (_x, _y, _w, _h) in face_locations:
            if (_w**2 + _h**2)**0.5 < 200:
                fl.append((_x, _y, _w, _h))
        face_locations = fl
        del fl

        face_locations = [(int(_x/resize_k), int(_y/resize_k), int(_w/resize_k), int(_h/resize_k))
                          for (_x, _y, _w, _h) in face_locations]
        face_locations = [(_y, (_x+_w), (_y+_h), _x)
                          for (_x, _y, _w, _h) in face_locations]
        face_encodings = face_recognition.face_encodings(rgb, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                encodings, face_encoding, tolerance=0.55)
            name = "-1"
            if True in matches:
                first_match_index = matches.index(True)
                name = ids_enc[first_match_index]
            face_names.append(name)
        last_names[1:ln_count] = last_names[0:ln_count-1]
        last_names[0] = face_names

        # anim_now = "rg"
        d_c = 0
        for fn in last_names:
            for name in fn:
                if name != "-1":
                    d_c += 1
        print(d_c)
        if get_last_name("george"):
            anim_now = "geor"
        elif get_last_name("vas59"):
            anim_now = "sin_g"
        elif get_last_name("m"):
            anim_now = "sin_b"
        elif get_last_name("-1"):
            anim_now = "rb"
        elif (d_c / ln_count) > 0.6:
            anim_now = "rg"
        else:
            anim_now = "rgb_v1"
        # if (d_c / ln_count) > 0.6:
        #     anim_now = "sin_r"
        # else:
        #     anim_now = "rgb_v1"

        for fb, name, i in zip(face_locations, face_names, range(len(face_names))):
            box = face_box_to_xyxy(fb)
            cv2.rectangle(resultImage, box[0], box[1],
                          (0, 0, (i/len(face_names))*255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(resultImage, name,
                        (box[0][0]+3, box[0][1]-1), font, 0.4, (255, 255, 255), 1)

        cv2.imshow("resultImage", resultImage)

    i += 1
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
dev.stop()
