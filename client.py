from socket import *
import cv2 
import pickle
import struct
import keyboard
from PIL import ImageGrab

serverName = '127.0.0.1'
serverPort = 10000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
frame = b""
payload = struct.calcsize("Q")

while True:
    while(len(frame) < payload):
        pkt = clientSocket.recv(10000)
        if not pkt:
            break
        frame+=pkt

    packed = frame[:payload]
    frame = frame[payload:]

    msg = struct.unpack("Q", packed)[0]
    while(len(frame) < msg):
        frame += clientSocket.recv(10000)

    readFrame =  frame[:msg]
    frame=frame[msg:]
    framePresent = pickle.loads(readFrame)
    cv2.imshow('client frame', framePresent) 

    if keyboard.is_pressed('space'):
        SS = ImageGrab.grab()
        save_path = f"path\\screenshot.jpg"
        SS.save(save_path)

    key = cv2.waitKey(1) & 0xFF 
    # keep the window until the key is pressed in a given time, i.e. 1
    # 0xFF is to avoid some bug of the key, normally 0-255
    if key  == ord('q'):
        break

clientSocket.close()
cv2.destroyAllWindows()