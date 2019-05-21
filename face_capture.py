"""
Face Data Capture Module
Capture 15 user's images
Store the images into the folder named with the username
"""
import os

import cv2


class FaceDataCapture:
    @staticmethod
    def capture(username):
        """
        Capture user's face data and save the pics into the same named folder
        :param username: capture the specific user's face data
        """

        # use name as folder name
        folder = "./dataset/{}".format(username)

        # Create a new folder for the new name
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Start the camera
        cam = cv2.VideoCapture(0)
        # Set video width
        cam.set(3, 640)
        # Set video height
        cam.set(4, 480)
        # Get the pre-built classifier that had been trained on 3 million faces
        face_detector = cv2.CascadeClassifier("Face_Classifier.xml")

        img_counter = 1
        # Capture maximum 15 picture
        while img_counter <= 15:
            key = input("Press q to quit or ENTER to continue: ")
            if key == "q":
                break

            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                print("No face detected, please try again")
                continue

            for (x_axis, y_axis, weight, height) in faces:
                cv2.rectangle(frame, (x_axis, y_axis), (x_axis + weight, y_axis + height), (255, 0, 0), 2)
                img_name = "{}/{:04}.jpg".format(folder, img_counter)
                cv2.imwrite(img_name, frame[y_axis: y_axis + height, x_axis: x_axis + weight])
                print("NO.{} image recorded!".format(img_counter))
                img_counter += 1

        cam.release()
