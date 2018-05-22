#!/usr/bin/python3

# Libs
from socket import socket, AF_INET, SOCK_STREAM
import pickle

"""The server receive the objectives coord, the robots coord, the move list and
the configuration filename from a client.

Objectives coord and robots coord must fit in a CHUNK_SIZE char long string,
and the move list has no limitation in size, but will be sent in chunks of
CHUNK_SIZE bytes.
Once the last message is received, the server disconnect and parse the data
received in order to give it to the simulator.

Packets identifiers (first 2 char of each message):
#c -> config file name (must be the same on both sides)
#1 -> coord. objectives
#2 -> coord. static objectives
#3 -> coord. robots
#4 -> move list
#0 -> End of communication
"""

CHUNK_SIZE = 4096  # Maximum message size the server can receive


def string_to_dict(message):
    """Convert a message containing coordinates to a dictionnary."""
    dic = {}
    obj_list = message[2:].split(',')
    for obj in obj_list:
        temp = obj.split(' ')
        dic[temp[0]] = (int(temp[1]), int(temp[2]))
    return dic


def string_to_movelist(message):
    """Convert a message containing a move list to a list"""
    move_list = message[2:].split(',')
    return move_list


def dispatcher(s):
    """Accept a connection with the planner, return data for initialization."""
    sClient, adrClient = s.accept()
    return handleClient(sClient, adrClient)


def receive_conf_list(s):
    sClient, adrClient = s.accept()
    recv_data = sClient.recv(CHUNK_SIZE)
    conf_list = pickle.loads(recv_data)
    sClient.close()
    return conf_list


def handleClient(sClient, adrClient):
    """Receive messages from the client (planner), convert them to
    readable datas for the simulator.
    """
    objectives_coord = {}
    static_obj_coord = {}
    robots_coord = {}
    move_list = []
    config_file = ""

    while True:
        message = sClient.recv(CHUNK_SIZE).decode()
        if not message:
            break
        message_id = message[:2]
        if message_id == '#0':
            break
        elif message_id == '#1':
            objectives_coord = string_to_dict(message)
        elif message_id == '#2':
            static_obj_coord = string_to_dict(message)
        elif message_id == '#3':
            robots_coord = string_to_dict(message)
        elif message_id == '#4':
            move_list += string_to_movelist(message)
        elif message_id == '#c':
            config_file = message[2:]
        # else:
        #     conf_list = pickle.loads(message)
        #     print(len(conf_list))
        #     input()

        sClient.send("OK".encode())
    sClient.close()
    return objectives_coord, static_obj_coord, \
        robots_coord, move_list, config_file


def start_server(IPAdr='127.0.0.2', port=5000):
    """Start the server, wait for connection, receive datas for the simulator
    and return them. Close the socket before returning.
    """
    s = socket(AF_INET, SOCK_STREAM)
    host = (IPAdr, port)
    s.bind(host)
    s.listen(1)
    conf_list = receive_conf_list(s)
    print(conf_list)
    input()
    objectives_coord, static_obj_coord, \
        robots_coord, move_list, config_file = dispatcher(s)
    s.close()
    return objectives_coord, static_obj_coord,\
        robots_coord, move_list, config_file


if __name__ == '__main__':
    objectives_coord, static_obj_coord, robots_coord, \
        move_list, config_file = start_server()
