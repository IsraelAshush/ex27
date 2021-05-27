#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol
import glob
import os
import shutil
import subprocess
import pyautogui

# from PIL import Image


IP = "127.0.0.1"
# PHOTO_PATH = r"C:\Networks\Pyhton3.8\gitme\net\ex27\photo_server"  # The path + filename where the screenshot at the
# server should be saved
SCREENSHOT_PATH = r"C:\Networks\Pyhton3.8\gitme\net\ex27\photo_server\screenshot.jpg"


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    if not protocol.check_cmd(cmd):
        return False
    # Then make sure the params are valid
    list_cmd = cmd.split()
    command = list_cmd[0]
    if command == "DELETE" or command == "DIR" or command == "EXECUTE" or command == "COPY":
        if not os.path.exists(list_cmd[1]):
            return False, command, list_cmd[1:]
    """elif command == "PHOTO_SEND" or command == "TAKE_SCREENSHOT":
        return True, command, []"""
    # (6)
    return True, command, list_cmd[1:]


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = 'FATAL'
    if command == 'DIR':
        path = r'%s' % params
        response = glob.glob(path)
    elif command == 'DELETE':
        path = r'%s' % params
        if os.remove(path):
            response = 'OK'
    elif command == 'EXECUTE':
        path = r'%s' % params
        if not os.path.exists(path):
            response = 'FILE NOT EXIST'
            return response
        if subprocess.call(path):
            response = 'OK'
    elif command == 'COPY':
        path_old = r'%s' % params[0]
        path_new = r'%s' % params[1]
        if shutil.copy(path_old, path_new):
            response = 'OK'
    elif command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        if image.save(SCREENSHOT_PATH):
            response = 'OK'
    elif command == 'SEND_PHOTO':
        size = os.stat(SCREENSHOT_PATH).st_size
        response = size

    # (7)

    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    (client_socket, client_address) = server_socket.accept()
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(str(response).encode())
                if command == 'SEND_PHOTO':
                    # Send the data itself to the client
                    with open(SCREENSHOT_PATH, 'rb') as send_image:
                        client_socket.send(send_image.read())
                    # (9)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                response = protocol.create_msg(response)
                client_socket.send(response)
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            response = protocol.create_msg(response)
            client_socket.send(response)
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()


if __name__ == '__main__':
    main()
