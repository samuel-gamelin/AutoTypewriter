import mss
import numpy
import pytesseract
import time
import win32api

from pyautogui import hotkey, press, typewrite

class AutoTypewriter():
    def __init__(self, x1, y1, x2, y2):
        self.box = (x1, y1, x2, y2)
        self.sct = mss.mss()
    
    def get_text(self):
        return pytesseract.image_to_string(numpy.asarray(self.sct.grab(self.box)), config='--psm 6 --oem 3')
    
    def typeout(self, text):
        #typewrite(text, 0.00000000000001) # Insane speed
        typewrite(text, 0.00000000000001) # Semi-realistic speed
        press('space')


def main():
    box = []

    while True:
        state_left = win32api.GetKeyState(0x01)
        if state_left == -127 or state_left == -128:
            xclick, yclick = win32api.GetCursorPos()
            box.append(xclick)
            box.append(yclick)
            print(xclick, yclick)
            break
    
    time.sleep(0.15)

    while True:
        state_left = win32api.GetKeyState(0x01)
        if state_left == -127 or state_left == -128:
            xclick, yclick = win32api.GetCursorPos()
            box.append(xclick)
            box.append(yclick)
            print(xclick, yclick)
            break

    print(box[0], box[1], box[2], box[3])

    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    writer = AutoTypewriter(box[0], box[1], box[2], box[3])
    time.sleep(.75)
    #initial_text = None
    for i in range(1):
        text = writer.get_text()
        #if initial_text == text:
            #break
        writer.typeout(writer.get_text())
        #initial_text = text
        hotkey('tab', 'enter')
        #print(writer.get_text())


if __name__ == '__main__':
    main()
