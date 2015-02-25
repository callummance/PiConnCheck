import socket
import threading
import time
import os
import sender
#!/usr/bin/env python

import socket, threading

def dencrypt(msg, key):
    return (bytearray([a ^ b for a, b in zip(msg,key)]))

class ClientThread(threading.Thread):
    state = "LOADING"
    key = None
    lastMessage = 0
    name = "PI"

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket

    def run(self):    
        print ("Connection from : " +ip+ ":" + str(port))
        self.key = self.csocket.recv(2048)
        data = "dummydata"

        while len(data):
            data = self.csocket.recv(2048)
            self.procMessage(data)

        print ("Client at "+self.ip+" disconnected...")

    def procMessage(self, data):
        '''print ("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data))'''
        decMess = str(dencrypt(data, self.key), "utf-8")
        status = decMess[0]
        msgTime = float(decMess[1:])
        currentTime = time.time()
        if status == "F":
            self.state = "ALERT"
        elif status == "T" and (currentTime - msgTime) <= maxTime and (currentTime - msgTime) >= 0:
            self.state = "all_clear"
            self.lastMessage = msgTime
        
            

#Device settings:
#============================================================    
#This pi's IP address and the intended port
host = "127.0.0.1"
port = 5005

#The expected number of other devices
noDevices = 1

#The maximum allowable delay
maxTime = 0.5

#The IP addresses of all other pis
ips = ["127.0.0.1"]

#The key which will be used by this pi
key = bytearray(os.urandom(18))
#=============================================================




#Initialize the server
#=========================
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))

srvStat = "LOADING"
#=========================



#Stores a list of all current connections
devices = []
targets = []



def checkConns(srvStat, devices, maxTime):
    print("Server status is now " + srvStat)
    curTime = time.time()

    for device in devices:
        if device.state == "LOADING":
            return "LOADING"
        elif curTime - device.lastMessage >= maxTime:
            return "ALERT: connection failure from " + device.name
        elif not(device.state == "all_clear"):
            return "ALERT from " + device.name
        elif srvStat == "LOADING" and device.state == "all_clear":
            return "ALL_CLEAR"
        else:
            return srvStat

def updateDevices(targets):
    for target in targets:
        target.sendPack()


for device in ips:
    targets.append(sender.stillAlive(device, port, key))

while True:
    updateDevices(targets)
    time.sleep(0.1)

while len(devices) < noDevices:
    tcpsock.listen(4)
    print ("\n" + str(len(devices)) + " are now connected.")
    print ("Server status is now " + srvStat)
    print ("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()

    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
    devices.append(newthread)




srvStat = "ALL_CLEAR"
while True:
    srvStat = checkConns(srvStat, devices, maxTime)
    updateDevices(targets)
    time.sleep(0.1)

