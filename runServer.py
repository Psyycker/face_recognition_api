import threading
import time
from multiprocessing import Process
import os
from src import app
from src import find_faces_in_picture_cnn
import face_recognition
import logging, multiprocessing



class ThreadManager:
    queue = []
    lock = threading.Lock()

    objectDict = [None, None, None, None]

    def addValueInQueue(self, filename, tmpFileName):

        print("coucou")

        self.lock.acquire()

        try:
            print("on entre dans le try")
            tmpDic = dict()
            tmpDic["filename"] = filename
            tmpDic["tmpFileName"] = tmpFileName

            self.queue.append(tmpDic)

            print(self.queue)

        finally:
            self.lock.release()

        return

    def writeInLog(self, number, text):
        file = open("logs/log" + str(number), "a")

        file.write(text + '\n')

        file.close()

    def addingPictureThread(self, number):



        print("Thread {} just started".format(number))

        while True:
            print("On passe")
            self.writeInLog(number, "On passe dans la boucle while")
            self.askStart(number)
            if self.objectDict[number] is not None:
                self.writeInLog(number,"On débute une analyse de picture")
                print("Thread {} starting picture analyse".format(number))
                find_faces_in_picture_cnn.find_faces(self.objectDict[number][0], self.objectDict[number][1])
                self.objectDict[number] = None
                self.writeInLog(number,"On fini une analyse de picture")
                print("Thread {} finished face analysis".format(number))

            #if (len(object) > 0):
            #    time.sleep(5)

            time.sleep(1)




    def __init__(self):

        print("Init")


        if os.path.exists("queue") is False:
            os.mkdir("queue")

        if os.path.exists("pictures") is False:
            os.mkdir("pictures")

        print("initialisation du thread manager")
        threading.Thread(target=self.addingPictureThread, kwargs=dict(number=0)).start()
        threading.Thread(target=self.addingPictureThread, kwargs=dict(number=1)).start()
        threading.Thread(target=self.addingPictureThread, kwargs=dict(number=2)).start()
        threading.Thread(target=self.addingPictureThread, kwargs=dict(number=3)).start()



    #Ask for a new object to include
    def askStart(self, number):
        self.lock.acquire()
        try:

            list = os.listdir("queue")

            if (len(list) > 0):
                self.writeInLog(number, "La liste est supérieure à 0")
                image = face_recognition.load_image_file("queue/" + list[0])

                self.objectDict[number] = [image, list[0]]
                os.remove("queue/" + list[0])
                self.writeInLog(number, "On a fini")
        finally:
            self.lock.release()




def startFlaskThreaded():
    print("démarrage du serveur flask")
    app.run(
        '127.0.0.1',
        5445
    )

def startThreadManager():
    threadManager = ThreadManager()
    while (True):
        time.sleep(1)

def main():
    threading.Thread(target=startFlaskThreaded).start()
    #threading.Thread(target=startThreadManager).start()
    Process(target=startThreadManager).start()
    while(True):
        time.sleep(1)

if __name__ == '__main__':
    main()