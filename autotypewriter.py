import argparse
import mss
import numpy
import platform
import pyperclip
import pytesseract
import sys
import time
import windows_keys
import win32api

from pyautogui import hotkey, press, typewrite
from typing import List

class AutoTypewriter():
    def __init__(self, ending_type: str, ending_keystrokes: List[str], interval: float, delay: float, lang: str, repeat: bool, bypass_anticheat:bool, box: tuple) -> None:
        self.ending_type = ending_type
        self.ending_keystrokes = ending_keystrokes
        self.interval = interval
        self.delay = delay
        self.lang = lang
        self.repeat = repeat
        self.bypass_anticheat = bypass_anticheat
        self.box = box
        self.sct = mss.mss()

        self.typeout = self.typeout_eng if self.lang == 'eng' else self.typeout_non_eng
    
    def get_text(self) -> str:
        return pytesseract.image_to_string(numpy.asarray(self.sct.grab(self.box)), self.lang, config='--psm 6 --oem 3')
    
    def typeout_eng(self, text: str) -> None:
        typewrite(text, self.interval)
        self.typeout_endings()

    def typeout_non_eng(self, text: str) -> None:
        """
        Types out non-english text. To circumvent limitations in pyautogui, the text is copied to the clipboard and pasted.
        """

        windows_keys.typewrite(text, self.interval)
        self.typeout_endings()
    
    def typeout_endings(self) -> None:
        if self.ending_type == 'press':
            press(*self.ending_keystrokes)
        elif self.ending_type == 'hotkey':
            hotkey(*self.ending_keystrokes)
        time.sleep(self.delay)
    
    def type_without_repeat(self) -> None:
        for _ in range(1):
            self.typeout(self.get_text())

    def type_with_repeat(self) -> None:
        initial_text = ''
        while True:
            text = self.get_text()
            if initial_text == text:
                break
            self.typeout(text)
            initial_text = text
    
    def copy_and_paste_text(self) -> None:
        text = self.get_text()
        pyperclip.copy(text)
        hotkey("ctrl", "v")
        self.typeout_endings()
    
    def do(self) -> None:
        if self.bypass_anticheat:
            self.copy_and_paste_text()
        elif self.repeat:
            self.type_with_repeat()
        else:
            self.type_without_repeat()

def main():
    sys.tracebacklimit = 0

    ending_types = ['press', 'hotkey']

    parser = argparse.ArgumentParser(description='Command line options for the typewriter')
    parser.add_argument('-t', '--ending-type', type=str, default='press', help="The type of keystroke to perform after typing out a sequence of text. Default is 'press'.")
    parser.add_argument('-k', '--ending-keystrokes', nargs='+', help="The keystroke(s) to type out, provided as a space-separated list. If one or more keystrokes are provided,\
        this option must be used in conjunction with an ending type of 'hotkey'. Default is 'space'.", default=['space'])
    parser.add_argument('-d', '--delay', type=float, default=0.0, help='The delay to add after typing out a block of text. Default is 0.0')
    parser.add_argument('-i', '--interval', type=float, default=0.0, help='The interval between each keystroke when typing out text, in seconds. Default is 0.0')
    parser.add_argument('-l', '--lang', type=str, default='eng', help='The language that is to be used to identify text. Must be provided as a language code specified by Tesseract.\
        Default: eng')
    parser.add_argument('--repeat', action='store_true', default=False, help='Specifying this flag will cause the script to keep taking screenshots after writing out a block of text\
        specified in the bounding box until that text stops changing. Once the text has stopped changing, this would indicate that the typing test is over.')
    parser.add_argument('-b', '--bypass-anticheat', action='store_true', default=False, help='Specifying this flag will make the typewriter attempt to bypass anticheat mechanisms by\
        copying the entirety of the displayed text in the bounding box once to the clipboard and pasting it.')
    
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

    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    
    writer = AutoTypewriter(args.ending_type, args.ending_keystrokes, args.interval, args.delay, args.lang, args.repeat, args.bypass_anticheat, tuple(box))
    
    time.sleep(1)

    writer.do()

if __name__ == '__main__':
    main()
