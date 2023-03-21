'''Библиотека для работы с файлами json'''
import json

'''Библиотеки для работы с реальным временем'''
import socket
import struct

'''Константы'''
from secondary_vars import MONTHS

def open_json(file):
    with open(file, "r", errors='ignore') as f:
        return json.load(f)


def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_time():
    address = ('pool.ntp.org', 123)
    msg = '\x1b' + '\0' * 47

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(bytes(msg, encoding='utf-8'), address)
    msg, _ = client.recvfrom(1024)

    secs = struct.unpack("!12I", msg)[10] - 2208988800
    return secs


def format_date(date):
    new_date = date
    new_date = f'{str(new_date).split("-")[2]} {MONTHS[int(str(new_date).split("-")[1]) - 1]}'
    if new_date[0] == '0':
        new_date = new_date[1:]
    return new_date


def fill_dict(**kwargs):
    param = dict()
    for key, value in kwargs.items():
        param[key] = value
    return param