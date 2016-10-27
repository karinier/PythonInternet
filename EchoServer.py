#!/usr/bin/env python3
# See https://docs.python.org/3.2/library/socket.html
# for a decscription of python socket and its parameters
import socket

from threading import Thread
from argparse import ArgumentParser

BUFSIZE = 4096
CRLF = '\r\n'
OK = 'HTTP/1.1 200 OK{}{}{}'.format(CRLF, CRLF, CRLF)
METHOD_NOT_ALLOWED = 'HTTP/1.1 405 Method Not Allowed{}{}{}'.format(CRLF,CRLF,CRLF)


def handle_request(request):
    

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
    
    data = client_sock.recv(BUFSIZE)
    while data:
        
        handle_request(data)
        data = client_sock.recv(BUFSIZE)

    
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')


class EchoServer:
    def __init__(self, host, port):
        print('listening on port {}'.format(port))
        
        self.host = host
        self.port = port

        
        self.setup_socket()

        
        self.accept()

        self.sock.shutdown()
        self.sock.close()

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.bind((self.host, self.port))
        self.sock.listen(128)

    def accept(self):
        # here is the loop. This accepts connections and then creates
        # a new Thread to handle that connection.
        while True:
            (client, address) = self.sock.accept()

           
            th = Thread(target=client_talk, args=(client, address))
            th.start()


def parse_args():
    
    parser = ArgumentParser()

    
    parser.add_argument('--host', type=str, default='localhost',
                        help='specify a host to operate on (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=9001,
                        help='specify a port to operate on (default: 9001)')
    args = parser.parse_args()
    return (args.host, args.port)


if __name__ == '__main__':
   
    (host, port) = parse_args()

    
    EchoServer(host, port)


