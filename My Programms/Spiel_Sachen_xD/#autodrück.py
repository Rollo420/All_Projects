import pyautogui
import keyboard
import time

def press_right_mouse_button():
    print("start")
    time.sleep(5)
    print("5 sekl duch")
    pyautogui.mouseDown(button='right')

def release_right_mouse_button():
    pyautogui.mouseUp(button='right')

# Funktion zum Überprüfen, ob die Taste "q" gedrückt wurde
def check_for_q_key():
    return keyboard.is_pressed('q')

if __name__ == '__main__':
    press_right_mouse_button()

    while True:
        if check_for_q_key():
            release_right_mouse_button()
            break
