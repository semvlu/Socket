from socket import *
import cv2 
import pickle
import struct

serverPort = 10000
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(5)

while True:
    connectionSocket, addr = serverSocket.accept()
    vid = cv2.VideoCapture(0) 
    while vid.isOpened():
        ret, frame = vid.read() # ret: bool
        cv2.imshow('server frame', frame) 

        dump = pickle.dumps(frame) # return obj into byte stream
        stream = struct.pack("Q", len(dump)) + dump # Q: format char, C-Python, unsigned long long-integer
        connectionSocket.sendall(stream)

        key = cv2.waitKey(1) & 0xFF
        # keep the window until the key is pressed in a given time, i.e. 1
        # 0xFF is to avoid some bug of the key, normally 0-255
        if key ==ord('q'):
            client_socket.close()
            break
vid.release() 
cv2.destroyAllWindows() 
connectionSocket.close()