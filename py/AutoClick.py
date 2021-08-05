import sys, os
import pyautogui
import keyboard, re
import pyperclip
import time, ctypes
import win32gui, win32api
from PIL import Image

def setWindow():
    while True:
        handle = win32gui.FindWindow(None,'League of Legends')
        if handle!=0:
            break
        print('can not find LOL, please launch the game')
        print('or long press ESC to stop the code')
        if keyboard.is_pressed('ESC'):
            exit(1)
        time.sleep(1)
    print('Find the game')
    print('name:', win32gui.GetWindowText(handle))
    win32api.keybd_event(13, 0, 0, 0) #
    win32gui.ShowWindow(handle, 1)
    win32gui.SetForegroundWindow(handle)

def getInviteCode():
    code_lists = []
    file_name = 'invite_code.txt'
    if not os.path.isfile(file_name):
        print('you do not have invite_code.txt')
        sys.exit()
    f = open(file_name, 'r', encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        code_lists.append(re.findall('(LOL+\w{10})', line))
    f.close()
    return code_lists

def manually_set_loc(s):
    print(s + ', and press \'a\' to choose location')
    while True:
        if keyboard.is_pressed('a'):
            return pyautogui.position()
def detectPosition():
    while True:
        input_pos = pyautogui.locateCenterOnScreen('./src/inputbox.JPG', confidence=0.7)
        if input_pos != None:
            break
        print('can not find input position, please check the window')
        print('or long press space to set location manually')
        if keyboard.is_pressed('Space'):
            input_pos = manually_set_loc("Move your mouse to the input button")
            break
        time.sleep(1)
    while True:
        get_pos_1 = pyautogui.locateCenterOnScreen('./src/get.JPG', confidence=0.7)
        get_pos_2 = pyautogui.locateCenterOnScreen('./src/get1.JPG', confidence=0.7)
        if get_pos_1 != None:
            get_pos = get_pos_1
            break
        if get_pos_2 != None:
            get_pos = get_pos_2
            break
        print('can not find get button position, please check the window')
        print('or long press space to set location manually')
        if keyboard.is_pressed('Space'):
            get_pos = manually_set_loc("Move your mouse to the \'get\' button")
            break
        time.sleep(1)
    return [input_pos, get_pos]

def start_execute(code_lists, input_pos, get_pos):
    ok_flag = True
    delay = 0.5
    print('if want to stop the code before finish, long press the \'ESC\'')
    i = 0
    for code in code_lists:
        print(code[0])
        print(input_pos, get_pos)
        pyperclip.copy(code[0])
        pyautogui.click(input_pos)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.click(get_pos)
        time.sleep(delay)
        if ok_flag:
            ok_pos_1 = pyautogui.locateCenterOnScreen('./src/ok.jpg', confidence=0.7)
            if ok_pos_1 == None:
                print('can not find \'ok\' button position, please check the window')
                print('or long press space to set location manually')
                ok_pos_1 = manually_set_loc("Move your mouse to the \'ok\' button")
            pyautogui.click(ok_pos_1)
            time.sleep(delay)
            ok_pos_2 = pyautogui.locateCenterOnScreen('./src/ok.jpg', confidence=0.7)
            if ok_pos_2 == None:
                print('can not find \'ok\' button position, please check the window')
                print('or long press space to set location manually')
                ok_pos_2 = manually_set_loc("Move your mouse to the \'ok\' button")
            pyautogui.click(ok_pos_2)
            time.sleep(delay)
            ok_flag = False
        else:
            pyautogui.click(ok_pos_1)
            time.sleep(delay)
            pyautogui.click(ok_pos_2)
            time.sleep(delay)

        if keyboard.is_pressed('ESC'):
            return


def main():
    setWindow()
    code_lists = getInviteCode()
    [input_pos, get_pos] = detectPosition()
    start_execute(code_lists, input_pos, get_pos)

if __name__ == "__main__":
    main()