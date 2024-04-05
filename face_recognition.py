import cv2
import mysql.connector
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


class Face_Recognition:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")

        # This part is image labels setting start
        # first header image
        img = Image.open(r"C:\Users\faizankne\Documents\python_test-projects\Images_GUI\banner.jpg")
        img = img.resize((1366, 130), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        # set image as a label
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # background image
        bg1 = Image.open(r"Images_GUI\bg2.jpg")
        bg1 = bg1.resize((1366, 768), Image.ANTIALIAS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        # set image as a label
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # title section
        title_lb1 = Label(bg_img, text="Welcome to Face Recognition Panel", font=("verdana", 30, "bold"),
                          bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Create buttons below the section
        # -------------------------------------------------------------------------------------------------------------------
        # Training button 1
        std_img_btn = Image.open(r"Images_GUI\f_det.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.face_recog, image=self.std_img1, cursor="hand2")
        std_b1.place(x=600, y=170, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.face_recog, text="Face Detector", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=600, y=350, width=180, height=45)

        self.recognized_ids = set()  # Set to keep track of recognized student IDs

    # =====================Attendance===================

    def mark_attendance(self, i, r, n):
        if i not in self.recognized_ids:
            self.recognized_ids.add(i)

            with open("attendance.csv", "a", newline="\n") as f:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i}, {r}, {n}, {dtString}, {d1}, Present")

    # ================face recognition==================
    def face_recog(self):
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                if confidence > 77:
                    conn = mysql.connector.connect(user='root', password='root', host='localhost',
                                                   database='face_recoginition', port=3306)
                    cursor = conn.cursor()

                    cursor.execute("select Name from student where Student_ID=" + str(id))
                    n = cursor.fetchone()
                    n = n[0] if n else ""

                    cursor.execute("select Roll_No from student where Student_ID=" + str(id))
                    r = cursor.fetchone()
                    r = r[0] if r else ""

                    cv2.putText(img, f"Student_ID:{id}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"Name:{n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"Roll-No:{r}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)

                    # Mark attendance only once for each recognized face
                    self.mark_attendance(id, r, n)

                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 3)

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("clf.xml")

        videoCap = cv2.VideoCapture(0)

        while True:
            ret, img = videoCap.read()
            draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            cv2.imshow("Face Detector", img)

            if cv2.waitKey(1) == 13:
                break
        videoCap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
