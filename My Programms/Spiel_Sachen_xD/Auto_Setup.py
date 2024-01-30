#erstelle mit pyautogui das er im hintergrund das mein bildschioerm aufnimmt und wenn er ein bestiummtes fentser erkannt hat das er obenrecht amfentser das fenster schließt er soll warten bis das fenster auftaucht und sonnst niochts machen 





import pyautogui 

while True: 
    if pyautogui.locateOnScreen(r'C:\Users\vossj\close.png') is not None:
        pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\vossj\close.png'))
        pyautogui.hotkey('alt', 'f4')