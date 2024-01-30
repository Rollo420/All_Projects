from pickletools import pynone
from ssl import SSLWantReadError
from tkinter.messagebox import Message
from tracemalloc import start
import pyautogui
from time import sleep
import webbrowser
import os
import keyboard
from pynput.mouse import Button, Controller
from tkinter import Image, messagebox
from bs4 import BeautifulSoup
import urllib3

clear = lambda: os.system('cls')
clear()

maus = Controller()
start_sta = 1
start_fol = 0
r = urllib3.PoolManager()

name = input("Hallo, welchen Anime möchtest du gerne gucken?\n").replace(' ', '-').lower()
sta = input("Welche Staffel gucken Sie\n")
fol = int(input("Bis zur welcher Folge Möchten sie gucken? (Zahl muss großer als 1 sein!!!) \n"))
lan = int(input("Wie viele Minuten geht eine Folge?\n"))
mon_po = int(input("Auf welchem Monitor guckst du?\n"))

print("Debug0")

time = lan  *60


safe = ""
while (safe!="YES" and safe!="NO"):
    safe = input("Wollen sie bei der Letzten folge weiter machen?? (Yes or No)\n").upper()


answer = ""
while (answer!="YES" and answer!="NO"):
    answer = input("Werden nue Tabs geöffnet? (Yes or No)\n").upper()


       
print("debug1")

if safe == 'YES':


    ja = open("E:\\Programme\\Test\\test.txt")
    start_fol = ja.read()
    ja.close()
    start_fol = int(start_fol) + 1


while int(start_fol) < fol:

    zeit = lan * fol
    print("Sie gucken noch: "+ str(zeit) + " Minuten")

    start_fol = int(start_fol) + 1

    link = webbrowser.open_new_tab('https://aniworld.to/anime/stream/' + name +'/staffel-' + str(sta) + '/episode-' +str(start_fol))
    link2 = 'https://aniworld.to/anime/stream/' + str(name) +'/staffel-' + str(sta) + '/episode-' +str(start_fol)

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
    response = r.request("GET", link2, headers=headers)
    data = BeautifulSoup(response.data, 'html.parser')
    
    # find all with the image tag
    images = data.find_all('img', src="/public/img/german.svg")
    images2 = data.find_all('img', type="button")
    print('Number of Images: ', len(images))
    for image in images:
        print(image)
        print(images2)
    
    if len(images) != 1:
        print("Not Found")
        exit()
    else:
        print("Found")
    
    if len(images2) != 1:
        print("Not Found")
        exit()
    else:
        print("Found")
        
        images2 = pyautogui.click()

    sleep(2)
    ## Maus positionieren
    #if mon_po == 1:
    #   mon = maus.position = (969, 636)
    #else:
    #    mon = maus.position =(3206, 722)

    maus.scroll(0, -4.2)
    sleep(1)
    maus.click(Button.left, 1)

    print("Debug2")

    if answer == "YES":
        sleep(1)
        keyboard.press_and_release("Ctrl+w")
        sleep(1)


    elif answer == "NO":
        print("ok")
    

    print("Debug3")


    pyautogui.press("f")
    sleep(time)
    
    keyboard.press_and_release("Ctrl+w")

    with open('E:\\Programme\\Test\\test.txt', 'w') as f:
          f.write(str(start_fol))
    print("debug4")

    


print("Debug6")


