#!/usr/bin/python
# -*- coding: utf-8 -*- 

import socket
import os
import sys
import select

host = ''
port = 9896
backlog = 10
size = 20480000

#function to send file
def sendf(soc):
    print("sending")
    soc.send(b'file name: ')
    fname = soc.recv(size)  
    fname = fname.decode('utf-8')  
    file=open(fname,'rb')
    data=file.read()
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    soc.send(data)
    print('File sent')

#function to receive file
def recvf(soc):
    print("Recieving")
    data = soc.recv(size)
    user_input = input(data)
    soc.send(bytes(user_input , 'utf-8'))
    data = soc.recv(20480000)
    if user_input.endswith('.txt'):
        fileHandler = open('abc.txt','w')
    elif user_input.endswith('.pdf'):
        fileHandler = open('abc.pdf','w')
    elif user_input.endswith('.png'):
        fileHandler = open('abc.png','w')
    elif user_input.endswith('.bin'):
        fileHandler = open("abc.bin" , 'wb')
    
    if user_input.endswith('bin'):
        fileHandler.write(data)
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
    while 1:
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
                            if data == '\GET_FILE':
                                sendf(client)
                        except Exception as e:
                            print(e)
                        if data == '\CLOSE_SESSION':
                            print('session ended')
                            client.close()
                            break
                        user_input = input('fs> ')
                        client.send(bytes(user_input , 'utf-8'))
                        if user_input == '\GET_FILE':
                            recvf(client)
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

#function for client to connect     to listening client                
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
        if data == '\GET_FILE':
            sendf(soc)
        if data == '\CLOSE_SESSION':
            print('session ended')
            soc.close()
            break
        user_input = input('ft> ')
        soc.send(bytes(user_input , 'utf-8'))
        if  user_input == '\GET_FILE':
            recvf(soc)  
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
