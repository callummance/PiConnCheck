import socket, time, os

class stillAlive:
    keyTransmitted = False
    msgCode = "T"
    
    def __init__(self, targetIP, port, key):
        self.targetIP = targetIP
        self.port = port
        self.key = key



    def sendPack(self):
        curTime = str(time.time())
        message = self.msgCode + curTime
        bMessage = bytearray(message, "utf-8")
        try:
            if not self.keyTransmitted:
                #Setup connection
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.targetIP, self.port))
                self.sendMsg(self.key)
                self.keyTransmitted = True
            else:
                self.sendMsg(dencrypt(bMessage, self.key))
        except ConnectionRefusedError:
            print("Could not connect")
            return

    def sendMsg(self, msg):
        self.sock.sendall(msg)


def dencrypt(msg, key):
    return (bytearray([a ^ b for a, b in zip(msg,key)]))

'''TCP_IP = "127.0.0.1"
TCP_PORT = 5005
KEY = bytearray(os.urandom(18))

test = stillAlive(TCP_IP, TCP_PORT, KEY)
while 1:
    test.sendPack()
    time.sleep(0.1)'''
