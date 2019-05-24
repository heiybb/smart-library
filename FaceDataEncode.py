"""
Face Data Encode Module
Encode the users' images into appropriate format
All the user's images will be precessed

Acknowledgement
This code is adapted from:
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
"""

import os
import pickle

import cv2
import face_recognition
# import the necessary packages
from imutils import paths


class FaceDataEncode:
    """
    Provide the face data encode static method
    """

    @staticmethod
    def encode():
        """
        Encode the images into appropriate format
        :return: None
        """
        # grab the paths to the input images in our dataset
        print("[INFO] Quantifying faces...")
        image_paths = list(paths.list_images("dataset"))

        # initialize the list of known encodings and known names
        known_encodings = []
        known_names = []

        # loop over the image paths
        for (i, image_path) in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
            name = image_path.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                known_encodings.append(encoding)
                known_names.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": known_encodings, "names": known_names}

        with open("encodings.pickle", "wb") as encoded_file:
            encoded_file.write(pickle.dumps(data))
