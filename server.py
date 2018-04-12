#!/usr/bin/python3

from socket import *
import time

"""The server receive the objectives coord, the robots coord and the move list.
Objectives coord and robots coord must fit in a 2048 char long string, and the
move list has no limitation in size, but will be sent in chunks of 2048bytes.
Once the last message is received, the server disconnect and parse the data received
in order to give it to the simulator.
Packets identifiers (first 2 char of each message):
#1 -> coord. objectives
#2 -> coord. static objectives
#3 -> coord. robots
#4 -> move list
#0 -> End of communication"""

def string_to_dict(message):
    """Convert a message containing coordinates to a dictionnary."""
    dic = {}
    obj_list = message[2:].split(',')
    #print('Obj list : ' + str(obj_list))
    for obj in obj_list:
        temp = obj.split(' ')
        dic[temp[0]] = (int(temp[1]), int(temp[2]))
    return dic

def string_to_movelist(message):
    """Convert a message containing a move list to a list"""
    move_list = message[2:].split(',')
    return move_list


def dispatcher(s):
    """Accept a connection with the planner, receive and convert datas for initialization."""
# Accepte une connexion puis affiche l'adresse
    sClient, adrClient = s.accept()
    print("Connexion : " + adrClient[0] + ':' + str(adrClient[1]) + "-" + time.strftime("%H:%M:%S", time.localtime()))
    return handleClient(sClient, adrClient)

def handleClient(sClient, adrClient):
    objectives_coord = {}
    static_obj_coord = {}
    robots_coord = {}
    move_list = []

    while True:
        message = sClient.recv(2048).decode()
        if not message: break
        message_id = message[:2]
        if message_id == '#0': break
        elif message_id == '#1':
            objectives_coord = string_to_dict(message)
        elif message_id == '#2':
            static_obj_coord = string_to_dict(message)
        elif message_id == '#3':
            robots_coord = string_to_dict(message)
        elif message_id == '#4':
            move_list += string_to_movelist(message)

        sClient.send("OK".encode())
        #print(adrClient[0] + ':' + str(adrClient[1]) + "-" + time.strftime("%H:%M:%S", time.localtime()) + "->" + message)
    sClient.close() # Quand la connexion se termine, on ferme la socket associée à ce client
    return objectives_coord, static_obj_coord, robots_coord, move_list



def start_server():
    s = socket(AF_INET, SOCK_STREAM)
    host = ('127.0.0.2', 5000)
    s.bind(host) # Écoute à l'adresse et au port définis dans host
    s.listen(1) # On accepte 1 connexion au maximum

    objectives_coord, static_obj_coord, robots_coord, move_list = dispatcher(s)

    s.close()
    return objectives_coord, static_obj_coord, robots_coord, move_list

if __name__ == '__main__':
    objectives_coord, static_obj_coord, robots_coord, move_list = start_server()
