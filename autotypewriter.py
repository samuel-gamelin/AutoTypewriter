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

from paste import PasteEEClient
from pyautogui import hotkey, press, typewrite


class AutoTypewriter():
    def __init__(self, ending_type, ending_keystrokes, interval, delay, lang, repeat, bypass_anticheat, paste_ee_method, paste_token):
        self.ending_type = ending_type
        self.ending_keystrokes = ending_keystrokes
        self.interval = interval
        self.delay = delay
        self.lang = lang
        self.repeat = repeat
        self.bypass_anticheat = bypass_anticheat
        self.paste_ee_method = paste_ee_method
        self.paste_token = paste_token
        self.box = []
        self.sct = mss.mss()

        self.typeout = self.typeout_eng if self.lang == 'eng' else self.typeout_non_eng

    def get_text(self):
        return pytesseract.image_to_string(numpy.asarray(self.sct.grab(tuple(self.box))), self.lang, config='--psm 6 --oem 3')

    def typeout_eng(self, text):
        typewrite(text, self.interval)
        self.typeout_endings()

    def typeout_non_eng(self, text):
        windows_keys.typewrite(text, self.interval)
        self.typeout_endings()

    def typeout_endings(self):
        if self.ending_type == 'press':
            press(*self.ending_keystrokes)
        elif self.ending_type == 'hotkey':
            hotkey(*self.ending_keystrokes)
        time.sleep(self.delay)

    def type_without_repeat(self):
        self.typeout(self.get_text())

    def type_with_repeat(self):
        initial_text = ''
        while True:
            text = self.get_text()
            if initial_text == text:
                break
            self.typeout(text)
            initial_text = text

    def copy_and_paste_text(self):
        text = self.get_text()
        pyperclip.copy(text)
        hotkey("ctrl", "v")
        self.typeout_endings()

    def wait_for_mouse_click(self):
        while True:
            state_left = win32api.GetKeyState(0x01)
            if state_left == -127 or state_left == -128:
                break

    def do(self):
        if self.paste_ee_method:
            client = PasteEEClient(self.paste_token)

            paste_content = client.getLatestPasteContent()

            while not paste_content:
                print("Could not fetch latest paste content. Trying in half a second...")
                time.sleep(0.5)
                paste_content = client.getLatestPasteContent()

            print("Ready! Will start typing right after you click!")

            self.wait_for_mouse_click()
            self.typeout(paste_content)
        else:
            for _ in range(2):
                while True:
                    state_left = win32api.GetKeyState(0x01)
                    if state_left == -127 or state_left == -128:
                        xclick, yclick = win32api.GetCursorPos()
                        self.box.append(xclick)
                        self.box.append(yclick)
                        break

                time.sleep(0.2)

            if platform.system() == 'Windows':
                pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

            print("Bounding box has been selected. Will start typing when you click!")

            self.wait_for_mouse_click()

            if self.bypass_anticheat:
                self.copy_and_paste_text()
            elif self.repeat:
                self.type_with_repeat()
            else:
                self.type_without_repeat()


def main():
    ending_types = ['press', 'hotkey']

    parser = argparse.ArgumentParser(
        description='Command line options for the typewriter')
    parser.add_argument('-t', '--ending-type', type=str, default='press',
                        help="The type of keystroke to perform after typing out a sequence of text. Default is 'press'.")
    parser.add_argument('-k', '--ending-keystrokes', nargs='+', help="The keystroke(s) to type out, provided as a space-separated list. If one or more keystrokes are provided,\
        this option must be used in conjunction with an ending type of 'hotkey'. Default is 'space'.", default=['space'])
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='The delay to add after typing out a block of text. Default is 0.0')
    parser.add_argument('-i', '--interval', type=float, default=0.0,
                        help='The interval between each keystroke when typing out text, in seconds. Default is 0.0')
    parser.add_argument('-l', '--lang', type=str, default='eng', help='The language that is to be used to identify text. Must be provided as a language code specified by Tesseract.\
        Default: eng')
    parser.add_argument('--repeat', action='store_true', default=False, help='Specifying this flag will cause the script to keep taking screenshots after writing out a block of text\
        specified in the bounding box until that text stops changing. Once the text has stopped changing, this would indicate that the typing test is over.')
    parser.add_argument('-b', '--bypass-anticheat', action='store_true', default=False, help='Specifying this flag will make the typewriter attempt to bypass anticheat mechanisms by\
        copying the entirety of the displayed text in the bounding box once to the clipboard and pasting it.')
    parser.add_argument('-p', '--paste', action='store_true', default=False, help='Specifying this flag will make the typewriter use the paste.ee method. A valid paste.ee API key needs\
        to be provided with --paste-token. Can only be used in conjunction with the accompanying Chrome extension on 10fastfingers.com.')
    parser.add_argument('--paste-token', type=str,
                        help='A valid paste.ee API token.')

    args = parser.parse_args()

    if args.ending_type not in ending_types:
        raise RuntimeError('Invalid ending type "' + args.ending_type +
                           '". Must be one of: ' + ', '.join(ending_types) + '.')
    elif args.ending_type == 'press' and len(args.ending_keystrokes) != 1:
        raise RuntimeError(
            'You cannot provide more than one keystroke when using the press ending type.')
    elif args.paste and not args.paste_token or args.paste_token and not args.paste:
        raise RuntimeError(
            'The --paste and --paste-token options accompany each other.')

    writer = AutoTypewriter(args.ending_type, args.ending_keystrokes, args.interval, args.delay,
                            args.lang, args.repeat, args.bypass_anticheat, args.paste, args.paste_token)

    writer.do()


if __name__ == '__main__':
    main()
