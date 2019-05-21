#!/usr/bin/env python3
"""
Socket utils
Include the send json data and receive json data
"""
import json
import struct


def send_json(socket, object):
    """
    Wrap the data to json format and send to the remote side
    :rtype: object
    :param socket: income socket used to send data
    :param object: income object prepare to convert to socket stream
    """
    try:
        json_string = json.dumps(object)
        data = json_string.encode("utf-8")
        json_length = struct.pack("!i", len(data))
        socket.sendall(json_length)
        socket.sendall(data)
    except socket.error:
        print("Can't handle send function")


def recv_json(socket):
    """
    Receive the json data and convert it
    :param socket: income socket used to receive data
    :return: json
    """
    try:
        buffer = socket.recv(4)
        json_length = struct.unpack("!i", buffer)[0]
    except socket.error:
        print("Can't handle receive function")
    else:
        # Reference: https://stackoverflow.com/a/15964489/9798310
        buffer = bytearray(json_length)
        view = memoryview(buffer)
        while json_length:
            nbytes = socket.recv_into(view, json_length)
            view = view[nbytes:]
            json_length -= nbytes

        json_string = buffer.decode("utf-8")
        return json.loads(json_string)
