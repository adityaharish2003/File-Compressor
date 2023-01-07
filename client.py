#!/usr/bin/python
# -*- coding: utf-8 -*- 

import socket
import os
import sys
import select
import time
import  multiprocessing.pool
import  functools

host = ''
port = 9896
backlog = 10
size = 4096


def timeout(max_timeout):
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


#function to send file
def sendf(soc):
    print("sending")
    fname = input("File Name: ")
    soc.send(bytes(fname , 'utf-8'))
    fileHandler = open(fname,'rb')
    fileHandler.seek(0)
    data = fileHandler.read()
    if not isinstance(data, bytes):
        print("ISSUE")
        data = data.encode('utf-8')
    soc.sendall(data)
    print('File sent')
    fileHandler.close()

@timeout(5.0)
def timeout_recv(soc , size):
    return soc.recv(size)

#function to receive file
def recvf(soc):
    print("Recieving")
    filename = soc.recv(size).decode('utf-8')
    if filename.endswith('.txt'):
        fileHandler = open('abc.txt','w')
    elif filename.endswith('.pdf'):
        fileHandler = open('abc.pdf','w')
    elif filename.endswith('.png'):  
        fileHandler = open('abc.png','w')
    elif filename.endswith('.bin'):
        fileHandler = open("abc.bin" , 'wb')
    if filename.endswith('bin'):
        while True:
            try:
                recvdata = timeout_recv(soc , size)
                fileHandler.write(recvdata)
                if not recvdata: break
            except multiprocessing.context.TimeoutError:
                break
    else:    
        fileHandler.write(str(data.decode('utf-8')))
    fileHandler.close()
    print('File received')

#function for client to listen for other client connections
def clisten(user_input):
    print("IN LISTEN")
    cport = int(user_input)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #binding the socket to localhost and port
    s.bind((host,cport))
    print('listening')
    s.listen(backlog)
    clist=[s]
    while True:
    # Using Select to handle multiplexing
        inready,outready,exceptready = select.select(clist,[],[])
        for sock in inready:
            if sock == s:
                client, address = s.accept()
                clist.append(client)
                print('connected')
                client.send(b'Start typing')
            else:
                try:
                    data = sock.recv(size)
                    data = data.decode('utf-8')
                    if data:
                        print()
                        print(data)
                        try:
                            if data == '\SEND_FILE':
                                recvf(client)
                        except Exception as e:
                            print(e)
                        if data == '\CLOSE_SESSION':
                            print('session ended')
                            client.close()
                            break
                        user_input = input('fs> ')
                        client.send(bytes(user_input , 'utf-8'))
                        if user_input == '\SEND_FILE':
                            sendf(client)
                            print("Sent file")     
                        if user_input == '\CLOSE_SESSION':
                            print('session ended')
                            client.close()
                            break
                except:
                    client.close()
                    input.remove(client)
                    #continue                
    return             

#function for client to connect to listening client                
def cconnect(data):
    print("IN CONNECT")
    cport = int(data)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        soc.connect((host,cport))
    except:
        print('Unable to connect to client')
    print('now connected')
    while True:
        data = soc.recv(size)
        data = data.decode('utf8')
        print(data)
        if data == '\SEND_FILE':
            recvf(soc)
        if data == '\CLOSE_SESSION':
            print('session ended')
            soc.close()
            break
        user_input = input('ft> ')
        soc.send(bytes(user_input , 'utf-8'))
        if  user_input == '\SEND_FILE':
            sendf(soc) 
        if user_input == '\CLOSE_SESSION':
            print('session ended')
            soc.close()
            break
    return

#main to handle connection between server and client
def main():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # try:
    sock.connect((host,port))
    # except:
    #     print('Unable to connect to chat server')
    #     sys.exit()
    while True:
        data = sock.recv(size)
        if data.isdigit() and int(data)>2000:
            cconnect(data)
        user_input = input(data)
        user_input = bytes(user_input , 'utf-8')
        sock.send((user_input))
        if user_input.isdigit() and int(user_input)>2000:
            clisten(user_input)
        if user_input == '\DISCONNECT_CLIENT':
            sock.close()
            break
        print()

if __name__ == '__main__':
    sys.exit(main())
