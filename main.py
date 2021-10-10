import numpy as np
import cv2
from mss import mss
from PIL import ImageGrab
import time
from pynput.keyboard import Key, Controller
import pyautogui

#hello world

keyboard = Controller()

mon = {'left': 220, 'top': 165, 'width': 1000, 'height': 610}

pos = 2

sct = mss()

cars = [False,False,False,False, False]

lowcolor = (0,0,100)
highcolor =(255,255,255)

def fixlook(pos):
    if pos == 2:
        return 0
    if pos == 0:
        return -2
    if pos == 1:
        return -1
    if pos == 3:
        return 1
    if pos == 4:
        return 2

def moveleft():
    keyboard.press(Key.left)
    time.sleep(0.1)
    keyboard.release(Key.left)
def moveright():
    keyboard.press(Key.right)
    time.sleep(0.1)
    keyboard.release(Key.right)

def checkCollision(pos, cars):
    if cars[pos + fixlook(pos)] == True:
        if pos == 4:
            moveleft()
            pos-=1
        if pos == 0:
            moveright()
            pos+=1
        else:
            moveleft()
            pos-=1

while True:
    sct_img = sct.grab(mon)
    img = np.array(sct_img)
    frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    parts = [frame[732:739, 1015-155:1022-155],frame[732:739, 1015-95:1022-95],frame[732:739, 1015:1022],frame[732:739, 1015+50:1022+50],frame[732:739, 1015+110:1022+110]]
    for i in range(5):

        average = cv2.mean(cv2.inRange(parts[i], lowcolor, highcolor))[0]
        if average == 0:
            cars[i] = False
        else:
            cars[i] = True


    if True in cars:
        print('car')
        
    checkCollision(pos, cars)
    cv2.rectangle(frame, (1015,732), (1022,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015-95,732), (1022-95,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015-155,732), (1022-155,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015+50,732), (1022+50,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015+110,732), (1022+110,739), (255,0,0), 2)
    cv2.imshow('screen', frame)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break