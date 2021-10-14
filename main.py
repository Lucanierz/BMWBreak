import numpy as np
import cv2
from mss import mss, tools
import time
from pynput.keyboard import Key, Controller
import pyautogui
from utils import tupop
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


keyboard = Controller()
fac = 2
mon = {'left': pyautogui.size()[0]/2-500, 'top': 0, 'width': 1000, 'height': 610}
mon_ = {'left': 0, 'top': 0, 'width': pyautogui.size()[0], 'height': pyautogui.size()[1]}
pos = 2
timer = 0
pressed = False
sct = mss()
cars = [False, False, False, False, False]

lowcolor = (0, 0, 100)
highcolor = (255, 255, 255)


def start_game():
    """uses selenium to automatically start game"""
    # start browser in fullscreen
    chromeOptions = Options()
    chromeOptions.add_argument("--kiosk")
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome("./webdriver/chromedriver", options=chromeOptions)

    # open game
    driver.get("https://aktion.bmw.de/bmw-bev-und-phev-gewinnspiel/bmw-points-challange/game.html")
    time.sleep(4)

    # start game
    button_coords = tupop((0.5, 0.95), pyautogui.size(), 2)
    for _ in range(3):
        pyautogui.click(button_coords)
        time.sleep(1)

    # tutorial screen
    time.sleep(20)


def start_game_():
    """uses selenium to automatically start game"""
    # start browser in fullscreen
    chromeOptions = Options()
    chromeOptions.add_argument("--kiosk")
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome("./webdriver/chromedriver", options=chromeOptions)

    # open game
    driver.get("https://aktion.bmw.de/bmw-bev-und-phev-gewinnspiel/?src=7")
    game = driver.find_element_by_id("game")
    driver.execute_script("arguments[0].scrollIntoView();", game)
    time.sleep(4)

    # start game
    button_coords = (0.5*pyautogui.size()[0], 590)
    for _ in range(3):
        pyautogui.click(button_coords)
        time.sleep(1)

    # tutorial screen
    time.sleep(20)


def fixlook(p):
    """handles car position offset"""
    if p == 2:
        return 0
    if p == 0:
        return +2
    if p == 1:
        return +1
    if p == 3:
        return -1
    if p == 4:
        return -2


def check_collision(p, c):
    """detects collision with other cars and moves accordingly"""
    if c[1]:
        global pos
        if p == 4:
            keyboard.press(Key.left)
            pos -= 1
        if p == 0:
            keyboard.press(Key.right)
            pos += 1
        else:
            keyboard.press(Key.left)
            pos -= 1
        return True
    else: return False
    # return cars[pos + fixlook(pos)]


if __name__ == '__main__':
    start_game_()
    while True:
        # print(pos)
        # print(pos)
        col = [(255, 0, 0), (255, 0, 0), (255, 0, 0)]
        sct_img = sct.grab(mon)
        img = np.array(sct_img)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        headlight = {
            'x': 483 * fac,
            'y': 402 * fac,
            'w': 10,
            'h': 10,
            'd': 55 * fac
        }
        """
        headlight = {
            'x': int(0.97 * pyautogui.size()[0]),
            'y': int(1.32 * pyautogui.size()[1]),
            'w': 10,
            'h': 10,
            'd': int(0.1 * pyautogui.size()[0])
        }
        
        parts = [
            frame[732:739, 1015-155:1022-155],
            frame[732:739, 1015-95:1022-95],
            frame[732:739, 1015:1022],
            frame[732:739, 1015+50:1022+50],
            frame[732:739, 1015+110:1022+110]
        ]
        """
        parts = [
            frame[headlight['y']:headlight['y'] + headlight['h'],
            headlight['x'] - headlight['d']:(headlight['x'] + headlight['w']) - headlight['d']],
            frame[headlight['y']:headlight['y'] + headlight['h'],
            headlight['x']:headlight['x'] + headlight['w']],
            frame[headlight['y']:headlight['y'] + headlight['h'],
            headlight['x'] + headlight['d']:(headlight['x'] + headlight['w']) + headlight['d']],
        ]
        for i in range(3):
            average = cv2.mean(cv2.inRange(parts[i], lowcolor, highcolor))[0]
            if average == 0:
                cars[i] = False
                col[i] = (255, 0, 0)
            else:
                cars[i] = True
                # print(cv2.mean(cv2.inRange(parts[i], lowcolor, highcolor))[0])
                col[i] = (0, 0, 255)

        # if True in cars:
            # print(int(cars[0]), int(cars[1]), int(cars[2]))

        if not pressed:
            if check_collision(pos, cars):
                pressed = True
                timer = time.time()
                # print("pressdown")

        if pressed and 0.2 < time.time() - timer < 0.5:
            keyboard.release(Key.left)
            keyboard.release(Key.right)
            pressed = False
            # print("pressup")

        headlight_pos = tupop((0.97, 1.32), (1000, 610), 2)
        headlight_size = (10, 10)
        headlight_dist = 0.11 * 1000
        cv2.rectangle(frame, headlight_pos, tupop(headlight_pos, headlight_size, 0), col[1], 2)
        cv2.rectangle(frame,
                      tupop(headlight_pos, (headlight_dist, 0), 1),
                      tupop(tupop(headlight_pos, (headlight_dist, 0), 1), headlight_size, 0), col[0], 2)
        cv2.rectangle(frame,
                      tupop(headlight_pos, (headlight_dist, 0), 0),
                      tupop(tupop(headlight_pos, (headlight_dist, 0), 0), headlight_size, 0), col[2], 2)

        cv2.namedWindow("sr", cv2.WINDOW_NORMAL)
        cv2.moveWindow("sr", -1440, 0)
        cv2.resizeWindow('sr', 1000, 610)
        cv2.imshow('sr', frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
