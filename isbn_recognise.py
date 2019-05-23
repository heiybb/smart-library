"""
Barcode Recognise Module
Scan the book's isbn code and convert it to number string
"""

import time

import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar


class BarcodeRecognise:
    """
    Provide the barcode recognise method
    pass the result to server end
    """

    @staticmethod
    def recognise():
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] Barcode Searching...")
        video_stream = VideoStream(src=0).start()
        time.sleep(2.0)
        found = set()
        # loop over the frames from the video stream
        attempt_count = 0
        while attempt_count <= 20:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = video_stream.read()
            frame = imutils.resize(frame, width=400)

            # find the barcode in the frame and decode each of the barcode
            barcode_set = pyzbar.decode(frame)

            # loop over the detected barcode
            for barcode in barcode_set:
                # the barcode data is a bytes object so we convert it to a string
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                # if the barcode text has not been seen before print it and update the set
                if (barcode_data not in found) and (barcode_type == 'EAN13'):
                    print("[ISBN FOUND] {}".format(barcode_data))
                    found.add(barcode_data)
                    video_stream.stop()
                    return barcode_data

            # wait a little before scanning again
            time.sleep(1)
        # close the output CSV file do a bit of cleanup
        print("[INFO] cleaning up...")


if __name__ == "__main__":
    BarcodeRecognise.recognise()
