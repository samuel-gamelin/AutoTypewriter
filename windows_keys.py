# Source: https://gist.github.com/ubershmekel/4b414a66037feaea595b5f4e78220aad

import ctypes
import pyautogui
import time
import sys

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

VK_RETURN = 0x0D                # ENTER key

UNICODE_TO_VK = {
    '\r': VK_RETURN,
    '\n': VK_RETURN,
}

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def send_input(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

def input_structure(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')

def keyboard_input_unicode(code, flags=0):
    flags = KEYEVENTF_UNICODE | flags
    return KEYBDINPUT(0, code, flags, 0, None)

def keyboard_input_vk(code, flags=0):
    return KEYBDINPUT(code, code, flags, 0, None)

def keyboard_event_unicode(code, flags=0):
    return input_structure(keyboard_input_unicode(code))

def keyboard_event_vk(code, flags=0):
    return input_structure(keyboard_input_vk(code, flags))

def press_vk(code):
    send_input(keyboard_event_vk(code, flags=0))

def press(character):
    if character in UNICODE_TO_VK:
        return press_vk(UNICODE_TO_VK[character])
    elif character == ' ':
        pyautogui.press('space')
        return
    code = ord(character)
    send_input(keyboard_event_unicode(code))

def typewrite(text: str, interval: float) -> None:
    for character in text:
        press(character)
        time.sleep(interval)