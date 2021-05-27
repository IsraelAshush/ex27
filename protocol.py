#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820
LIST_COMMAND = ['DIR', 'DELETE', 'COPY', 'EXECUTE', 'SEND_PHOTO', 'TAKE_SCREENSHOT', 'EXIT']


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    try:
        stream = str(data).split()
        if stream[0] not in LIST_COMMAND:
            return False
        if (stream[0] == "DELETE" or stream[0] == "DIR" or stream[0] == "EXECUTE") and (len(stream) != 2):
            return False
        if (stream[0] == "COPY") and (len(stream) != 3):
            return False
        if (stream[0] == "SEND_PHOTO" or stream[0] == "TAKE_SCREENSHOT") and (len(stream) != 1):
            return False
    except:
        print("Error Args")
        return False
    # (3)
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    length = str(len(data))
    length_zipped = length.zfill(4)  # (4) bytes for length protocol
    message = length_zipped + data
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(4).decode()
    if not length.isdigit():
        return False, "Error"
    message = my_socket.recv(int(length))
    # (5)
    return True, message
