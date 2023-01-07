#!/usr/bin/python
# -*- coding: utf-8 -*- 

import socket
import os
import sys
import select

host = ''
port = 9896
backlog = 10
size = 2048
temp = 0

#function for help command
def usage(client):
    msg= '''
Command List:

\GET_CLIENT_LIST – to request list of connected clients

\GET_CLIENT_INFO <username> - to receive listening socket of the client to connect to

\DISCONNECT_CLIENT –  to indicate that you are no longer connected to the chat service\n'''
    client.send(msg)

#to store username and password in dictionary, to register user
def store(client,dict_,uname,pswd,c_info):
    if uname in dict_.keys():
        client.send(b'username is already taken. Type "Y" to set new username\n')
    else:
        dict_[uname]=pswd
        corl(client,c_info,uname)
        client.send(b'\nType your request or type \help for help\n')

#to check if username and password is present in dictionary, to authenticate user
def check(client,dict_,uname,pswd,c_info):
    pswd = pswd.decode('utf-8')
    if uname in dict_.keys() and dict_[uname] == pswd:
        client.send((bytes(f'Welcome back {uname.decode("utf-8")}\n' , 'utf-8')))
        corl(client,c_info,uname)
        temp = 0
    else:
        client.send(b'Incorrect username or password! Try again\n')
        temp = 1
    print(dict_)
    return temp

#ask if client wants to listen for connections or connect to existing client
def corl(client,c_info,uname):
    client.send(b'Do you want to "connect" or "listen"? ')
    resp = client.recv(size)
    resp =resp.decode('utf-8')
    if resp == 'listen':
        client.send(b'Enter your listening port: ')
        cport = client.recv(size)
        cport = cport.decode('utf-8')
        c_info[uname] = cport

#provides client_info i.e. listening port
def info(client,c_info):
    client.send(b'username: ')
    uname = client.recv(size)
    # uname = uname.decode('utf-8')
    print(uname)
    print(c_info)
    if uname in c_info:
        client.send(bytes(c_info[uname] , 'utf-8'))
        #log[uname]
    else:
        client.send(b'Incorrect username')

#function to process requests from client
def start(client,input,dict,c_info,log):
    try:
        data = client.recv(size)
        data  = data.decode('utf-8')
        if data == 'y' or data == 'Y':    #requests new username and password if new user
            client.send(b'Set new username & password\nusername: ')
            uname = client.recv(size)
            client.send(b'password: ')
            pswd = client.recv(size)
            pswd = pswd.decode('utf-8')
            store(client,dict,uname,pswd,c_info)
        
        elif data == 'n' or data == 'N':   #if existing user, it verifies the username and password
            for x in range(0, 3):          #provides three attempts for user to login
                client.send(b'Type your username and password\nusername: ')
                uname = client.recv(size)
                # uname = uname.decode('utf-8')
                client.send(b'password: ')
                pswd = client.recv(size)
                if check(client,dict,uname,pswd,c_info)==0:
                    client.send(b'\nType your request or type \help for help\n')
                    break
                if x == 2:
                    client.send(b'You have exceeded the no. of retries')        
                
        if data == '\help':                 #if help command is given
            usage(client)    

        if data =='\GET_CLIENT_LIST':       #send list of connected clients to user
            output = f'\CLIENT_LIST: {str(dict.keys())}' 
            client.send(bytes(output , 'utf-8'))

        if data =='\GET_CLIENT_INFO':       #sends listening port of client
            info(client,c_info) 

        if data == '\DISCONNECT_CLIENT':    #disconnect client if requested
            client.close()
            input.remove(client)

        else:
            pass
    except Exception as e:
        print(e)
        client.close()
        input.remove(client)
        
#main to create initial connection
def main():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #binding the socket to localhost and port
    sock.bind((host,port))
    sock.listen(backlog)
    input = [sock]
    dict = {}    #to store username and password
    c_info = {}  #to store username and port nos.
    log = {}     #to store chat sessions
    print("Chat server is now running on port " + str(port))
    while True:
        # Using Select to handle multiplexing
        inready,outready,exceptready = select.select(input,[],[])
        for s in inready:
            if s == sock:
                client, address = sock.accept()
                input.append(client)
                client.send(b'Are you a new user? Type Y or N: ')
            else:
                start(s,input,dict,c_info,log)

if __name__ == '__main__':
    main()
