#!/usr/bin/python3

from socket import *
import time, _thread

def dispatcher(s):
    while True:
# Accepte une connexion puis affiche l'adresse
        sClient, adrClient = s.accept()
        print("Connexion : " + adrClient[0] + ':' + str(adrClient[1]) + "-" + time.strftime("%H:%M:%S", time.localtime()))
# Lance un nouveau thread pour communiquer avec le client sur la socket créée à cet effet
        _thread.start_new(handleClient, (sClient, adrClient))

def handleClient(sClient, adrClient):
    while True:
        message = sClient.recv(1024).decode()
        if not message: break
# netcat envoie un retour à la ligne (\n) à la fin du message mais le client en python non
        sClient.send("Je vous ai compris".encode())
        print(adrClient[0] + ':' + str(adrClient[1]) + "-" + time.strftime("%H:%M:%S", time.localtime()) + "->" + message)
    sClient.close() # Quand la connexion se termine, on ferme la socket associée à ce client


def start_server():
    s = socket(AF_INET, SOCK_STREAM)
    host = ('127.0.0.2', 5000)
    s.bind(host) # Écoute à l'adresse et au port définis dans host
    s.listen(5) # On accepte 5 connexion au maximum

    dispatcher(s)

    s.close()


if __name__ == '__main__':
    start_server()