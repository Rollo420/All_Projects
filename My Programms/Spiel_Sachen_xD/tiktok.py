from selenium import webdriver
import time

bot = webdriver.Chrome()
bot.set_window_size(1680, 900)

bot.get('https://www.tiktok.com/upload/')
bot.add_cookie({'msToken': '5d4nPKju-gk4HdiTp6qNH7BRH61fEqD2X2nA'})

time.sleep(20)