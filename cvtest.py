
import math
import dlib, sys
import numpy as np
import cv2
import time
from tkinter import messagebox as mb
from tkinter import messagebox as tk

def facerec():
    truecounter = 0
    counter = 0
    scaler = 0.3
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    timeout = time.time() + 5
    while True:
        if time.time() > timeout:
            break
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (960, 540))
        cv2.putText(img, "Please keep smiling for 5 seconds.", (220, 30), 0, 0.7, (255,255,255), 2)

        #detect
        faces = detector(img)
        if not faces:
            cv2.putText(img, "Cannot Detect Face! Please center your face on the screen.", (170, 270)
                        , 0, 0.7, (255, 255, 255), 2)
            cv2.imshow('img', img)
            cv2.waitKey(1)
        else:
            face = faces[0]

            dlib_shape = predictor(img, face)
            shape_2d = np.array([[p.x, p.y] for p in dlib_shape.parts()])
            #visualize
            #img = cv2.rectangle(img, pt1=(face.left(), face.top()), pt2 = (face.right(), face.bottom()), color=(255,255,255),
             #                   thickness=2, lineType = cv2.LINE_AA)
            for s in shape_2d:
                cv2.circle(img, center=tuple(s), radius = 1, color=(255,255,255))

            leftEyeX = dlib_shape.part(40).x
            leftEyeY = dlib_shape.part(40).y
            rightEyeX = dlib_shape.part(47).x
            rightEyeY = dlib_shape.part(47).y

            lipRightX = dlib_shape.part(54).x
            lipRightY = dlib_shape.part(54).y
            lipLeftX = dlib_shape.part(48).x
            lipLeftY = dlib_shape.part(48).y

            leftDistance = math.sqrt((leftEyeX - lipLeftX)**2 + (leftEyeY - lipLeftY)**2)
            rightDistance = math.sqrt((rightEyeX - lipRightX)**2 + (rightEyeY - lipRightY)**2)
            cv2.line(img, (leftEyeX, leftEyeY), (lipLeftX, lipLeftY), (255,255,255), 1, cv2.LINE_AA, 0);
            cv2.line(img, (rightEyeX, rightEyeY), (lipRightX, lipRightY), (255, 255, 255), 1, cv2.LINE_AA, 0);


            cv2.putText(img, "left facial distance = "+str(int(leftDistance)) + "   right facial distance = "+str(int(rightDistance)), (200, 270)
                        , 0, 0.7, (255,255,255), 2)
            strokeIndex = bool(abs((leftDistance-rightDistance)/leftDistance)>0.045)
            cv2.putText(img, "FaceDroop = "+str(strokeIndex), (200, 230)
                        , 0, 0.7, (255, 255, 255), 2)
            if strokeIndex:
                truecounter += 1
                counter += 1
            else:
                counter += 1
            cv2.imshow('img', img)
            cv2.waitKey(1)
            if cv2.getWindowProperty('img', 4) < 1:
                break
    cv2.destroyAllWindows()
    return truecounter/counter

def armrec():

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    mb.showinfo('test info',
                "Please hold up your laptop for 10 seconds after pressing ok. Stay Still! Image may seem frozen. Test will close after it finishes.")
    time.sleep(2)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def takePic():
        ret, img = cap.read()

        img = cv2.resize(img, (960, 540))


        #detect
        faces = detector(img)
        while True:
            if faces:
                face = faces[0]
                break
            else:
                faces = detector(img)

        dlib_shape = predictor(img, face)

        X = [0, 0]
        X[0] = dlib_shape.part(34).x
        X[1] = dlib_shape.part(34).y

        return X

    initialCoord = takePic()
    time.sleep(10)
    finalCoord = takePic()

    Distance = math.sqrt((initialCoord[0] - finalCoord[0])**2 + (initialCoord[1] - finalCoord[1])**2)
    mb.showinfo('result', "Your distance was "+str(Distance)+" Pixels.")
    return Distance
