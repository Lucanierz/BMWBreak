import numpy as np
import cv2
from mss import mss
from PIL import ImageGrab
import time
from pynput.keyboard import Key, Controller
from selenium import webdriver
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def tupop(t1, t2, op):
    if op == 0:
        return tuple(int(a + b) for a, b in zip(t1, t2))
    elif op == 1:
        return tuple(int(a - b) for a, b in zip(t1, t2))
    elif op == 2:
        return tuple(int(a * b) for a, b in zip(t1, t2))
    elif op == 3:
        return tuple(int(a / b) for a, b in zip(t1, t2))


keyboard = Controller()


def start_game():
    # start browser in fullscreen
    chromeOptions = Options()
    chromeOptions.add_argument("--kiosk")
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome("./webdriver/chromedriver", options=chromeOptions)

    # open game
    driver.get("https://aktion.bmw.de/bmw-bev-und-phev-gewinnspiel/bmw-points-challange/game.html")
    time.sleep(5)

    # start game
    # button_coords = tuple(p * size for p, size in zip((0.5, 0.95), pyautogui.size()))
    button_coords = tupop((0.5, 0.95), pyautogui.size(), 2)
    for _ in range(3):
        pyautogui.click(button_coords)
        time.sleep(1)


mon = {'left': 220, 'top': 165, 'width': 1000, 'height': 610}
pos = 2
sct = mss()
cars = [False, False, False, False, False]

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


def check_collision(pos, cars):
    if cars[pos + fixlook(pos)]:
        if pos == 4:
            moveleft()
            pos -= 1
        if pos == 0:
            moveright()
            pos += 1
        else:
            moveleft()
            pos -= 1


while True:
    img = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    headlight = {
        'x': int(0.97 * pyautogui.size()[0]),
        'y': int(1.32 * pyautogui.size()[1]),
        'w': 10,
        'h': 10,
        'd': int(0.1 * pyautogui.size()[0])
    }
    """
    parts = [
        frame[732:739, 1015-155:1022-155], 
        frame[732:739, 1015-95:1022-95], 
        frame[732:739, 1015:1022],
        frame[732:739, 1015+50:1022+50], 
        frame[732:739, 1015+110:1022+110]
    ]
    """
    parts = [
        frame[headlight['y']:headlight['y']+headlight['h'], headlight['x'] - headlight['d']*2:(headlight['x'] + headlight['w']) - headlight['d']*2],
        frame[headlight['y']:headlight['y']+headlight['h'], headlight['x'] - headlight['d']:(headlight['x'] + headlight['w']) - headlight['d']],
        frame[headlight['y']:headlight['y']+headlight['h'], headlight['x']:headlight['x'] + headlight['w']],
        frame[headlight['y']:headlight['y']+headlight['h'], headlight['x'] + headlight['d']:(headlight['x'] + headlight['w']) + headlight['d']],
        frame[headlight['y']:headlight['y']+headlight['h'], headlight['x'] + headlight['d']*2:(headlight['x'] + headlight['w']) + headlight['d']*2]
    ]
    for i in range(5):

        average = cv2.mean(cv2.inRange(parts[i], lowcolor, highcolor))[0]
        if average == 0:
            cars[i] = False
        else:
            cars[i] = True

    if True in cars:
        print('car')
        
    # check_collision(pos, cars)
    """
    cv2.rectangle(frame, (1015,732), (1022,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015-95,732), (1022-95,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015-155,732), (1022-155,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015+50,732), (1022+50,739), (255,0,0), 2)
    cv2.rectangle(frame, (1015+110,732), (1022+110,739), (255,0,0), 2)
    """
    headlight_pos = tupop((0.97, 1.32), pyautogui.size(), 2)
    headlight_size = (10, 10)
    headlight_dist = 0.1 * pyautogui.size()[0]
    c = (255, 0, 0)

    cv2.rectangle(frame, headlight_pos, tupop(headlight_pos, headlight_size, 0), c, 2)
    cv2.rectangle(frame,
                  tupop(headlight_pos, (headlight_dist, 0), 1),
                  tupop(tupop(headlight_pos, (headlight_dist, 0), 1), headlight_size, 0), c, 2)
    cv2.rectangle(frame,
                  tupop(headlight_pos, (headlight_dist*2, 0), 1),
                  tupop(tupop(headlight_pos, (headlight_dist*2, 0), 1), headlight_size, 0), c, 2)
    cv2.rectangle(frame,
                  tupop(headlight_pos, (headlight_dist, 0), 0),
                  tupop(tupop(headlight_pos, (headlight_dist, 0), 0), headlight_size, 0), c, 2)
    cv2.rectangle(frame,
                  tupop(headlight_pos, (headlight_dist*2, 0), 0),
                  tupop(tupop(headlight_pos, (headlight_dist*2, 0), 0), headlight_size, 0), c, 2)

    cv2.namedWindow("sr", cv2.WINDOW_NORMAL)
    cv2.moveWindow("sr", -1440, 0)
    cv2.resizeWindow('sr', 1440, 810)
    cv2.imshow('sr', frame)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
