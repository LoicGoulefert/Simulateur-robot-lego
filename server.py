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

# Global variables
CHUNK_SIZE = 4096  # Maximum message size the server can receive


def string_to_dict(message):
    """Convert a message containing coordinates to a dictionnary.

    Parameters:
        message: string representing coords.
    """
    dic = {}
    obj_list = message[2:].split(',')
    for obj in obj_list:
        temp = obj.split(' ')
        dic[temp[0]] = (int(temp[1]), int(temp[2]))
    return dic


def string_to_movelist(message):
    """Convert a message containing a move list to a list.

    Parameters:
        message: string representing a move list
    """
    move_list = message[2:].split(',')
    return move_list


def dispatcher(s, f):
    """Accept a connection with the planner and execute
    the function f.

    Parameters:
        s: socket
        f: function to execute
    """
    sClient, adrClient = s.accept()
    return f(sClient, adrClient)


def receive_conf_list(sClient, adrClient):
    """Receive and unpickle the conf_list. Returns it.

    Parameters:
        sClient: client socket
        adrClient: client adress
    """
    size = int(sClient.recv(CHUNK_SIZE))
    sClient.send("Got the size !".encode())
    recv_data = sClient.recv(size)
    sClient.send("Got the list !".encode())
    conf_list = pickle.loads(recv_data)
    sClient.close()
    print('Len conf list :', len(conf_list))
    return conf_list


def receive_infos(sClient, adrClient):
    """Receive messages from the client (planner), convert them to
    readable datas for the simulator.

    Parameters:
        sClient: client socket
        adrClient: client adress
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

        sClient.send("OK".encode())
    sClient.close()
    return objectives_coord, static_obj_coord, \
        robots_coord, move_list, config_file


def start_server(IPAdr='127.0.0.2', port=5000):
    """Start the server, wait for connection, receive datas for the simulator
    and return them. Close the socket before returning.

    Parameters:
        IPAdr: string representing the IP of the host
        port: integer, the port we're listening on
    """
    s = socket(AF_INET, SOCK_STREAM)
    host = (IPAdr, port)
    s.bind(host)
    s.listen(1)
    conf_list = dispatcher(s, receive_conf_list)

    objectives_coord, static_obj_coord, \
        robots_coord, move_list, config_file \
        = dispatcher(s, receive_infos)
    s.close()

    return objectives_coord, static_obj_coord,\
        robots_coord, move_list, config_file, conf_list


if __name__ == '__main__':
    objectives_coord, static_obj_coord, robots_coord, \
        move_list, config_file, conf_list = start_server()
