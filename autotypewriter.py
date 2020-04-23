import argparse
import keyboard
import mss
import numpy
import os
import pyperclip
import pytesseract
import sys
import time

from paste import PasteEEClient
from pynput import mouse


class AutoTypewriter():
    def __init__(self, ending_keystroke, interval, delay, lang, repeat, bypass_anticheat, paste_key):
        self.ending_keystroke = ending_keystroke
        self.interval = interval
        self.delay = delay
        self.lang = lang
        self.repeat = repeat
        self.bypass_anticheat = bypass_anticheat
        self.paste_key = paste_key
        self.box = []
        self.sct = mss.mss()
        self.in_selection_mode = True

    def get_text(self):
        """Returns the text in this typewriter's bounding box as a string."""
        return pytesseract.image_to_string(numpy.asarray(self.sct.grab(tuple(self.box))), self.lang, config='--psm 6 --oem 3')

    def typeout(self, text):
        """Types out the specified text."""
        for character in text:
            if character == ' ':
                keyboard.press('space')
                keyboard.release('space')
            else:
                keyboard.write(character)
            time.sleep(self.interval)
        self.typeout_ending_keystroke()

    def typeout_ending_keystroke(self):
        """Types out this typewriter's ending keystroke."""
        keyboard.press(self.ending_keystroke)
        keyboard.release(self.ending_keystroke)
        time.sleep(self.delay)

    def type_without_repeat(self):
        """Types out the text in this typewriter's bounding box only once, without taking any further screenshots."""
        self.typeout(self.get_text())

    def type_with_repeat(self):
        """Types out the text in this typewriter's bounding box, taking screenshots after this typerwriter's specified delay
        and typing out the text within that screenshot, repeating until the text no longer changes."""
        initial_text = ''
        while True:
            text = self.get_text()
            if initial_text == text:
                break
            self.typeout(text)
            initial_text = text

    def copy_and_paste_text(self):
        """Copies the text in this typewriter's bounding box to the clipboard and pastes it."""
        text = self.get_text()
        pyperclip.copy(text)
        keyboard.press("ctrl+v")
        keyboard.release("ctrl+v")
        self.typeout_ending_keystroke()

    def on_click_handler(self, x, y, button, pressed):
        """"An on click handler for the selection of the bounding box."""
        if self.in_selection_mode and pressed:
            self.box.append(x)
            self.box.append(y)
            print('Corner ' + str(int(len(self.box) / 2)) +
                  ' has been set at (' + str(x) + ', ' + str(y) + ')')
        if len(self.box) == 4:
            return False

    def wait_for_mouse_click(self):
        """Pauses the execution of the program until a mouse click is received."""
        def on_click(x, y, button, pressed):
            if pressed:
                return False

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def do(self):
        if self.paste_key:
            self.in_selection_mode = False
            client = PasteEEClient(self.paste_key)
            paste_content = client.getLatestPasteContent()

            while not paste_content:
                print("Could not fetch latest paste content. Trying in half a second...")
                time.sleep(0.5)
                paste_content = client.getLatestPasteContent()

            print("Ready! Will start typing right after you click!")

            self.wait_for_mouse_click()
            self.typeout(paste_content)
        else:
            print(
                "Please select the two corners for the bounding box by clicking with your mouse")

            try:
                pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_PATH"]
            except KeyError:
                raise RuntimeError(
                    "The environment variable TESSERACT_PATH is not defined!")

            with mouse.Listener(on_click=self.on_click_handler) as listener:
                listener.join()

            print(
                "Bounding box has been selected. Typing will start right after you click!")

            self.wait_for_mouse_click()

            if self.bypass_anticheat:
                self.copy_and_paste_text()
            elif self.repeat:
                self.type_with_repeat()
            else:
                self.type_without_repeat()


def main():
    parser = argparse.ArgumentParser(
        description='Command line options for the typewriter')
    parser.add_argument('-k', '--ending-keystroke', type=str, default='space',
                        help="The keystroke to type out after typing out a block of text, provided as a string. Examples: 'shift+tab', 'ctrl+v', 'tab'. Default is 'space'.")
    parser.add_argument('-d', '--delay', type=float, default=0.0,
                        help='The delay to add after typing out a block of text. Default is 0.0')
    parser.add_argument('-i', '--interval', type=float, default=0.0,
                        help='The interval between each keystroke when typing out text, in seconds. Default is 0.0')
    parser.add_argument('-l', '--lang', type=str, default='eng',
                        help='The language that is to be used to identify text. Must be provided as a language code specified by Tesseract. Default: eng')
    parser.add_argument('-r', '--repeat', action='store_true', default=False,
                        help='Specifying this flag will cause the script to keep taking screenshots after writing out a block of text specified in the bounding box until that text stops changing. Once the text has stopped changing,\
                            this would indicate that the typing test is over.')
    parser.add_argument('-b', '--bypass-anticheat', action='store_true', default=False,
                        help='Specifying this flag will make the typewriter attempt to bypass anticheat mechanisms on 10fastfingers.com by copying the entirety of the displayed text in the bounding box once to the clipboard and pasting it.')
    parser.add_argument('-p', '--paste-key', type=str,
                        help='Specifying this flag will make the typewriter use the paste.ee method, which drastically improves permances as it reduces the overhead of grabbing screenshots and performing OCR. Note: A valid paste.ee application\
                            key needs to be provided with this option.')

    args = parser.parse_args()

    writer = AutoTypewriter(args.ending_keystroke, args.interval, args.delay,
                            args.lang, args.repeat, args.bypass_anticheat, args.paste_key)

    writer.do()


if __name__ == '__main__':
    main()
