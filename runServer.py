import threading
import time
from multiprocessing import Process
import os
from flaskApi import app
from opencv import find_faces_in_picture_cnn
import face_recognition
import logging, multiprocessing


#TODO : Settings file to change number of threads for each work and update for dispatcher


class IndexManager:
    maxthreads = 4
    index = 0

    def increaseIndex(self):
        self.index += 1
        if (self.index == self.maxthreads):
            self.index = 0

indexManager = IndexManager()





def startFlask():
    print("démarrage du serveur flask")
    app.run(
        '127.0.0.1',
        5445
    )


def startSlave(port):
    print("Démarrage des slaves")
    os.system("python3 Runslave.py " + port)

def startComparingSlave(port):
    print("Démarrage d'un slave de comparaison")

def main():

    if not os.path.exists("tmp"):
        os.mkdir("tmp")

    Process(target=startSlave, kwargs=dict(port="6500")).start()
    Process(target=startSlave, kwargs=dict(port="6501")).start()
    Process(target=startSlave, kwargs=dict(port="6502")).start()
    Process(target=startSlave, kwargs=dict(port="6503")).start()

    startFlask()




if __name__ == '__main__':
    main()