import socket
import struct
import time

def get_message_from_sntp_server():
    sock = socket.socket()
    sock.connect(("localhost", 123))
    sock.send(str.encode('\x1b' + 47 * '\0'))
    return sock.recv(1024)

def print_time():
    data = get_message_from_sntp_server()
    try:
        time_now = struct.unpack("!12I", data)[10]
        print(time.ctime(time_now))
    except:
        pass

if __name__ == '__main__':
    print_time()