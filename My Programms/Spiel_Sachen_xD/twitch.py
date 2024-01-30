from msilib.schema import Control
import os
from queue import PriorityQueue
import pyautogui
import webbrowser
import time 
from pynput.mouse import Button, Controller
from msvcrt import getch

mouse = Controller()
print("Wo ist die 1. Position?\n\n")
time.sleep(5)
p = mouse.position
z = 0
s = int(input("wie Viele Spiens?\n"))
t = int(input("Wie lange soll ich warten?\n"))

while z < s:

  print(p , "\n")
  time.sleep(t)
  mouse.position = (p)
  mouse.click(Button.left)



