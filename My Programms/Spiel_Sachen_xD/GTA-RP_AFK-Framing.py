from re import I
import tkinter as tk
from tkinter.messagebox import Message
from turtle import clear
#from turtle import left
from pynput.mouse import Button, Controller
import time
import pyautogui
import json
import os
import winsound



print("█░░░█ █▀▀█ █▀▀█ █▀▀▄ █░░ █░░█ ░█▀█░ █▀█ █▀▀█\n█▄█▄█ █░░█ █░░█ █░░█ █░░ █▄▄█ █▄▄█▄ ░▄▀ █▄▀█\n░█░█░ ▀░░▀ ▀▀▀▀ ▀▀▀░ ▀▀▀ ▀░░▀░ ▀░▀▀░ ▀░▀ ▀░░▀\n░▀░▀░ ▀▀▀▀ ▀▀▀▀ ▀▀▀░ ▀▀▀ ▄▄▄█ ░░░█░ █▄▄ █▄▄█")

mouse = Controller()
zahl = 0
zeit = 20
fahr = int(input("Wie viel Kapazität hat das Fahrzeug?\n"))


print("Wo ist die 1. Position?\n\n")
time.sleep(5)
po1 = mouse.position
print(po1 , "\n") 
time.sleep(0.5)
print("Wo ist die 2. Position?\n")
time.sleep(5)
po2 = mouse.position
print(po2, "\n")
print("Wo ist die 3. Position?\n")
time.sleep(5)
po3 = mouse.position
print(po3, "\n")
print("Wo ist die 4. Position?\n")
time.sleep(5)
po4 = mouse.position
print(po4, "\n")


print ("Current position: " + str(mouse.position))
print("Processing started...\n")
kapa = fahr/10


#// answor yes or no record mouse position po4
answer = input("Arbeite Sie noch in einer aderne Anwendung??\n") 


while zahl <= kapa:

     #// calculate the time
    #// berechne die gesamt Zeit der anwenung in Minuten
    #// 
    ge_zeit = (int(kapa) * zeit) / 60
    
    #time.sleep(35) 
    if answer == "yes":
        print("Aktuelle Maus position: " + str(mouse.position)+"\n")
        po4 = mouse.position
    
    if answer == "no":
        print("ok")
    

    time.sleep(0.5)
    mouse.position = (po1)
    mouse.click(Button.left)
    time.sleep(0.1) 
    mouse.position = (po1)
   # mouse.position = (611, 296)
    mouse.press(Button.left)
    mouse.position = (po2)
   # mouse.position = (1149, 294)
    time.sleep(0.2)
    mouse.release(Button.left)
    time.sleep(1)
    
    mouse.position = (po3)
   # mouse.position = (611, 296)
    mouse.press(Button.left)
    mouse.position = (po4)
   # mouse.position = (1149, 294)
    time.sleep(0.5)
    mouse.release(Button.left)
    time.sleep(0.2)

    zahl += 1
   #if answer == "yes":
   #    pyautogui.press('windows')
   #    mouse.position = (po4) 
   #    mouse.click(Button.left)

    #//make a cowndown timer 35 sekunden
    #//make a counting down time 
    #// when the timer is over restart the timer
    while zeit > 0:
        time.sleep(1)
        zeit = zeit - 1
    
        #// clear the console with os.system("cls")
        clear = os.system("cls")
        #// print "zahl" and "zeit" in red color in text mode  
        # 
        print ("Die Gesammtzeit Beträgt: " + str(ge_zeit) + " Minuten")
        print("Sie sind beim "+ "\033[1;31;40m" + str(zahl) + "/" + str(kapa) + "\033[0;37;40m" + " durch lauf und in " + "\033[1;31;40m" + str(zeit) + " in " + "\033[0;37;40m" +  " ist der nächste durch lauf.")


    #restart the timer
    zeit = 20





