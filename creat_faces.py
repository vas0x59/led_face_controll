import cv2
import dlib
import threading
import time
import face_recognition
import pickle


faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(2)

# ret = True
resize_k = 0.9
while True:
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imshow("frame", frame)
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
    # print(face_locations)

    for (x, y, w, h) in face_locations:
        cv2.rectangle(resultImage, (x, y), (x+w, y+h), (0, 0, 255), 2)

    face_locations = [(_y, (_x+_w), (_y+_h), _x)
                      for (_x, _y, _w, _h) in face_locations]

    face_encodings = face_recognition.face_encodings(rgb, face_locations)
    print(face_encodings)

    cv2.imshow("resultImage", resultImage)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        name = input()
        enc = face_encodings[0]
        f = open('faces/' + '' + str(name) + '.pickle', 'wb')
        pickle.dump((str(name), enc), f)
        pass

cap.release()
cv2.destroyAllWindows()
