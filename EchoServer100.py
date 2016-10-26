#!/usr/bin/env python3
# See https://docs.python.org/3.2/library/socket.html
# for a decscription of python socket and its parameters
import socket

from threading import Thread
from argparse import ArgumentParser

BUFSIZE = 4096
CRLF = '\r\n'
OK = 'HTTP/1.0 200 OK{}{}{}'.format(CRLF, CRLF, CRLF)
METHOD_NOT_ALLOWED = 'HTTP/1.0 405 Method Not Allowed{}{}{}'.format(CRLF,CRLF,CRLF)


def handle_request(request):
    # here the request can be handled
    # right now it just takes the bytes that are received and
    # decodes them as utf-8 bytes and prints it out

    print(request.decode('utf-8'))
    lines = request.splitlines()
    head = lines[0]
    print(head)
    words = head.split()
    if words[0].decode("utf-8") == 'GET':
        print("We have a GET request!")
        return bytes(OK, "utf-8")
    elif words[0].decode("utf-8") == 'HEAD':
        print("We have a HEAD request!")
        return bytes(OK, "utf-8")

    elif words[0].decode("utf-8") == 'PUT':
        print("We have a  PUT request!")
    else:
        return bytes(METHOD_NOT_ALLOWED, "utf-8")


def client_talk(client_sock, client_addr):
    print('talking to {}'.format(client_addr))
    # it looks like it just receives connections
    # and then prints out what it received then

    # for more data to receive and prints it out
    # keeps looping doing that.
    data = client_sock.recv(BUFSIZE)
    while data:
        # here is where we need to handle the GET/HEAD requests
        # and everything basically.
        # a good way to do this is to make a function here, and pass
        # the data to it so that you can keep the logic separate.
        handle_request(data)
        data = client_sock.recv(BUFSIZE)

    # if the client (the remote side) disconnects then it falls to here
    # and this thread is cleaned up. This can be seen by closing the browser
    # tab or stopping the browser from loading the localhost:9001 page.
    # or by ctrl-c killing the curl command

    # clean up
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')


class EchoServer:
    def __init__(self, host, port):
        print('listening on port {}'.format(port))
        # the command line arguments host and port are assigned locally here
        # we have an Object/Class that is called EchoServer and we attach
        # this host and port to it, e.g. self.host = host will assign host to
        # this instance of the EchoServer class
        self.host = host
        self.port = port

        # okay, this is where the binding of the socket is done.
        # so that when we make connections to this host on this port
        # it will come to this socket
        self.setup_socket()

        # this is a loop to accept connections on that socket that we
        # just opened in setup_socket
        self.accept()

        self.sock.shutdown()
        self.sock.close()

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # it's bound to localhost and port 9001 by default
        self.sock.bind((self.host, self.port))
        self.sock.listen(128)

    def accept(self):
        # here is the loop. This accepts connections and then creates
        # a new Thread to handle that connection.
        while True:
            (client, address) = self.sock.accept()

            # it creates this thread then starts it and then loops back to waiting
            # for more connections while the Thread runs elsewhere.
            # client_talk is the handler function
            th = Thread(target=client_talk, args=(client, address))
            th.start()


def parse_args():
    # this is the parsing function
    parser = ArgumentParser()

    # default is localhost if no argument is given
    parser.add_argument('--host', type=str, default='localhost',
                        help='specify a host to operate on (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=9001,
                        help='specify a port to operate on (default: 9001)')
    args = parser.parse_args()
    return (args.host, args.port)


if __name__ == '__main__':
    # program starts here
    # parses the command line arguments -host and -port into those
    # variables host and port, if they are found.
    (host, port) = parse_args()

    # this is where the actual server part starts, in this function
    EchoServer(host, port)


