import time
from pynput.keyboard import Key, Controller
keyboard = Controller()
time.sleep(5)
print("slept")
def moveleft():
    keyboard.press(Key.left)
    time.sleep(0.1)
    keyboard.release(Key.left)
def moveright():
    keyboard.press(Key.right)
    time.sleep(0.1)
    keyboard.release(Key.right)
while True:
    moveleft()
    time.sleep(1)
    moveright()
    time.sleep(1)