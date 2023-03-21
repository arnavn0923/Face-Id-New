from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import face_recognition as fr
import cv2
from datetime import datetime
import os
import pandas as pd
from tkinter import ttk




path='C:/Users/arnav/Downloads/photos'
known_encodings = []
known_names = []
encodeList = []



def findEncodings():
    for file in os.listdir(path):
        img = cv2.imread(path + '/' + file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)
        known_encodings.append(encode[0])
        known_names.append(file.split('.')[0])
    # print(known_encodings)
    print(known_names)
    print('Encoded successfully')
findEncodings()


def markAttendance(name):
    with open('C:/Users/arnav/Downloads/attendance_list.csv','r+') as FILE:
        allLines = FILE.readlines()
        attendanceList = []
        for line in allLines:
            entry = line.split(',')
            attendanceList.append(entry[0])
        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            FILE.writelines(f'\n{name},{dtString}')


def  upload_picture():
        frame=cv2.imread(filename)
        frame=cv2.resize(frame,(800,800))
        rgb_frame = frame[:, :, ::-1]
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encondings, face_encoding)
            name = "Unkown Entity"
            face_distances = fr.face_distance(known_face_encondings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            markAttendance(name)
        cv2.imshow('Webcam_facerecognition', frame)


def live_camera():
    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(frame)
        face_encodings = fr.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_encodings, face_encoding)
            global namee

            namee = "Unkown Entity"

            face_distances = fr.face_distance(known_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                namee = known_names[best_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, namee, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            markAttendance(namee)

        cv2.imshow('Webcam_facerecognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# tkinter GUI
import tkinter as tk
root= tk.Tk()

#Make a Canvas (i.e, a screen for your project
canvas1 = tk.Canvas(root, width = 500, height = 500)
canvas1.pack()

canvas1.config(bg='light blue')

# Popularity label and input box
label1 = tk.Label(root, text='Face Recognition Attendance Marking System')
canvas1.create_window(250, 50, window=label1)

#Add button in GUI
button3 = tk.Button (root, text='Live',command=live_camera, bg='orange') # button to call the 'values' command above
canvas1.create_window(250, 200, window=button3)


root.mainloop()

