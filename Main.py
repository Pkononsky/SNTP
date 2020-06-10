import os
import socket
import struct
import sys
import time

magic_message = str.encode('\x1b' + 47 * '\0')
#номер версии, режим

def print_help():
    print("Сервер sntp")
    print("вывод спраки - python Main.py -h/--help")
    print("запуск:\npython Main.py")
    print("после запуска будет ожидать запрос от клиента:")
    print("python client.py")


def check_connection_to_network():
    try:
        sock = socket.socket()
        sock.connect(("www.google.com", 80))
        sock.close()
        return True
    except:
        return False


def get_message_from_ntp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(magic_message, ("0.ru.pool.ntp.org", 123))
    data, addr = sock.recvfrom(1024)
    unpacked_data = list(struct.unpack("!12I", data))
    return unpacked_data


def get_message_with_wrong_time():
    unpacked_data = get_message_from_ntp_server()
    time_from_1900 = unpacked_data[10]
    time_from_1970 = time_from_1900 - 2208988800
    data_from_file = open("conf.txt", mode="r").read()
    try:
        data_from_file = int(data_from_file)
    except:
        print("Ошибка записи числа в файле conf.txt")
        return b""
    wrong_time = time_from_1970 + int(open("conf.txt", mode="r").read())
    unpacked_data[10] = wrong_time
    return struct.pack("!12I", *unpacked_data)


def main():
    if not check_connection_to_network():
        print("Нет доступа в Интернет")
        os.abort()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 123))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            message = conn.recv(1024)
            if message == magic_message:
                conn.send(get_message_with_wrong_time())
            conn.close()
        finally:
            conn.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
        os.abort()
    if sys.argv[1] in ["-h", "--help"]:
        print_help()
        os.abort()
    if sys.argv[1] not in ["-h", "--help"]:
        print("Неверный аргумент")
        os.abort()
