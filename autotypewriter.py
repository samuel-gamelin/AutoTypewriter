import argparse
import mss
import numpy
import os
import pytesseract
import sys
import time
import win32api

from pyautogui import hotkey, press, typewrite

class AutoTypewriter():
    def __init__(self, ending_type, ending_keystrokes, interval, delay, repeat, box):
        self.ending_type = ending_type
        self.ending_keystrokes = ending_keystrokes
        self.interval = interval
        self.delay = delay
        self.repeat = repeat
        self.box = box
        self.sct = mss.mss()

        self.do = self.type_with_repeat if self.repeat else self.type_without_repeat 
    
    def get_text(self):
        return pytesseract.image_to_string(numpy.asarray(self.sct.grab(self.box)), config='--psm 6 --oem 3').replace('\n', ' ').replace('|', 'I')
    
    def typeout(self, text):
        typewrite(text, self.interval)
        if self.ending_type == 'press':
            press(*self.ending_keystrokes)
        elif self.ending_type == 'hotkey':
            hotkey(*self.ending_keystrokes)
        time.sleep(self.delay)
    
    def type_without_repeat(self):
        for _ in range(1):
            self.typeout(self.get_text())

    def type_with_repeat(self):
        initial_text = ''
        while True:
            text = self.get_text()
            if initial_text == text:
                break
            self.typeout(text)
            initial_text = text

def main():
    sys.tracebacklimit = 0

    ending_types = ['press', 'hotkey']

    parser = argparse.ArgumentParser(description='Command line options for the typewriter')
    parser.add_argument('-t', '--ending-type', type=str, default='press', help="The type of keystroke to perform after typing out a sequence of text. Default is 'press'.")
    parser.add_argument('-e', '--ending-keystrokes', nargs='+', help="The keystroke(s) to type out. If one or more keystrokes are provided, this option must be used in conjunction\
        with an ending type of 'hotkey'. Default is 'space'.", default=['space'])
    parser.add_argument('-d', '--delay', type=float, default=0.0, help='The delay to add after typing out a block of text. Default is 0.0')
    parser.add_argument('-i', '--interval', type=float, default=0.0, help='The interval between each keystroke when typing out text, in seconds. Default is 0.0')
    parser.add_argument('--repeat', action='store_true', default=False, help='Specifying this flag will cause the script to keep taking screenshots after writing out a block of text\
        specified in the bounding box until that text stops changing. Once the text has stopped changing, this would indicate that the typing test is over.')
    
    args = parser.parse_args()

    if args.ending_type not in ending_types:
        raise RuntimeError('Invalid ending type "' + args.ending_type + '". Must be one of: ' + ', '.join(ending_types) + '.')
    elif args.ending_type == 'press' and len(args.ending_keystrokes) != 1:
        raise RuntimeError('You cannot provide more than one keystroke when using the press ending type.')

    box = []

    for _ in range(2):
        while True:
            state_left = win32api.GetKeyState(0x01)
            if state_left == -127 or state_left == -128:
                xclick, yclick = win32api.GetCursorPos()
                box.append(xclick)
                box.append(yclick)
                break
        
        time.sleep(0.2)

    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    
    writer = AutoTypewriter(args.ending_type, args.ending_keystrokes, args.interval, args.delay, args.repeat, tuple(box))
    
    time.sleep(1)

    writer.do()

if __name__ == '__main__':
    main()
