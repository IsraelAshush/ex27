#   Ex. 2.7 complete - client side
#   Author: Israel Ashush, 2017
#   Modified for Python 3, 2020


import socket
import protocol
import server

IP = '127.0.0.1'
SAVED_PHOTO_LOCATION = r"C:\Networks\Pyhton3.8\gitme\net\ex27\photo_client\screenshot.jpg"  # The path + filename
# where the copy of the screenshot at the client should be saved


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    length = my_socket.recv(4).decode()
    # (10) treat SEND_PHOTO
    if cmd == 'SEND_PHOTO':
        length = my_socket.recv(int(length)).decode()
        image = my_socket.recv(int(length))
        with open(SAVED_PHOTO_LOCATION, 'wb') as output_file:
            output_file.write(image)
    else:
        data = my_socket.recv(int(length)).decode()
        if cmd == 'DIR':
            for file in data:
                print(file)
        else:
            print(data)


def main():
    # open socket with the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server.IP, protocol.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            client_socket.send(packet)
            handle_server_response(client_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    client_socket.close()


if __name__ == '__main__':
    main()
