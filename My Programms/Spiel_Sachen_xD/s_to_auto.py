import math
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httpx
from tqdm import tqdm

#downloade_path = r'E:\testSerie'
app_version = "1.0.0"


def download_mp4(url, destination, episode_title, episode_number):
    try:
        with httpx.stream('GET', url) as response:
            response.raise_for_status()  # Raise an HTTPError for bad responses

            filename = f'{episode_title}_Folge_{episode_number}.mp4'
            download_destination = os.path.join(destination, filename)  # Fix: Verwenden Sie 'destination' anstelle von 'downloade_path'

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte

            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Download von {filename}')

            with open(download_destination, 'wb') as file:
                for chunk in response.iter_bytes():  # Fix: Entfernen Sie 'chunk_size=block_size'
                    progress_bar.update(len(chunk))
                    file.write(chunk)

            progress_bar.close()
            print(f'Download von {url} abgeschlossen. Gespeichert als {filename}')
    except httpx.RequestError as e:
        print(f'Download von {url} fehlgeschlagen. Fehler: {e}')

def get_episode_title(soup):
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        return title.split('|')[0].strip()
    return 'Unknown_Title'

    

def get_src_link(url):
    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    profile = webdriver.FirefoxProfile()
    adblockfile = 'adblockplus-2.6.3.3846.xpi'
    profile.add_extension (adblockfile)
    profile.set_preference("extensions.adblockplus.currentVersion", "2.6.3")
    browser = webdriver.Firefox(firefox_profile=profile)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        src_link = soup.find('video').find('source').get('src')
        episode_title = get_episode_title(soup)
        
        if mode == 2:
            download_mp4(src_link, downloade_path, episode_title, actual_episode)  # Setzen Sie die Folgennummer entsprechend Ihrer Logik
        
        elif mode == 1:
            print(click_my_element(driver,'.vjs-big-play-button')) 
            print(click_my_element(driver,'.vjs-big-play-button')) 

            # Execute JavaScript to get the duration of the video
            try:
                video_duration = driver.execute_script("return document.querySelector('video').duration")

                video_duration = round(video_duration)
                print(video_duration)
                time.sleep(video_duration)
            
            except ValueError as ve:
                print(f'Die video länge konnte nicht ermittelt werden!!!\nError: {ve}')

        return src_link

    finally:
        driver.quit()

def find_My_element(driver, css_path: str):
    # Find the element based on the specified CSS selector
    element = WebDriverWait(driver, 20).until(  # Increase the wait time to 20 seconds
        EC.presence_of_element_located((By.CSS_SELECTOR, css_path))
    )
    return element

def click_my_element(driver, css_path):
    try:
        submit_Button = find_My_element(driver, css_path)
        driver.execute_script("arguments[0].click();", submit_Button)

        return f"Element: {submit_Button} clicked"
    except Exception as e:
        return f"I cant found Button"


def open_seit(url):
    global element, class_value

    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        element = soup.find("i", class_="icon Vidoza")

        if element:
            class_value = element.get("class")
            actual_link = Next_Folge(driver)
            return actual_link

    finally:
        driver.quit()

def Next_Folge(driver):
    for class_name in class_value:
        if class_name == "Vidoza":
            link_element = element.find_parent("a")
            href = link_element.get("href")
            actual_link = f'https://186.2.175.5{href}'

            get_src_link(actual_link)

            return actual_link


def check_input(input_value, data_type : str, ersatz_value = 1, punkt_out = ""):
    global logo

    logo = r"""
                               __   ___                
Copyright © 2024              /\ \ /\_ \               
 __  __  __    ___     ___    \_\ \\//\ \    __  __    
/\ \/\ \/\ \  / __`\  / __`\  /'_` \ \ \ \  /\ \/\ \   
\ \ \_/ \_/ \/\ \L\ \/\ \L\ \/\ \L\ \ \_\ \_\ \ \_\ \  
 \ \___x___/'\ \____/\ \____/\ \___,_\/\____\\/`____ \ 
  \/__//__/   \/___/  \/___/  \/__,_ /\/____/ `/___/> \
                                                 /\___/
                                                 \/__/ """

    os.system('cls')
   
    print(logo)
    

    while True:
        input_value = input(f"\n{input_value}\n  {punkt_out}• ").strip()
        
        try:
            if data_type == "int":
                if input_value == "":
                    input_value = ersatz_value
        
                return int(input_value)
            else:
                return str(input_value)
        except ValueError:
            print(f'Geben Sie {data_type} ein!!!')


def getInfo():
    
    #print(logo, '\n\n')
    name = check_input("Bitte geben Sie die Serie ein: ", 'str').strip().replace(" ", "-").lower() or "the-witcher"

    global mode
    mode = check_input(f'Möchte Sie {name.replace("-", " ")}:\n\n    1) Watch (defualt)\n    2) Downloade\n', data_type='int', punkt_out='1) or 2) ')
    start_folge = check_input('Ab welche Folge soll angefangen werden? (Press enter for 1)', 'int')
    want_to_watch = check_input('Wie viele Folgen möchten Sie? (Für alle Folgen geben Sie die letzte Folge der Staffel an)?', 'int')
    end_folge = start_folge + want_to_watch
    staffel = check_input('Welche Staffel möchten Sie? ?(Press Enter for Staffel 1)', 'int')

    if mode == 2:     
        global downloade_path
        # Bestimmt den Standard-Downloads-Ordner des Benutzers
        default_downloads_folder = os.path.expanduser(os.path.join("~", "Downloads"))

        #Wenn downloade_path nicht festgelegt ist, setze es auf den Standard-Downloads-Ordner
        downloade_path = input("\nWo sollen die Folgen Gespeichert werden? (Press enter to Default Downloadefolder) \n    • ") or default_downloads_folder


    os.system("cls")

    print(logo, '\n\n')

    
    for i in range(start_folge, end_folge):

        print(logo, '\n\n')

        show_folgen = i - start_folge 
        print(f"Sie haben: {show_folgen +1} / {want_to_watch}")
        #url = f'https://s.to/serie/stream/{name}/staffel-1/episode-{i}'  # Aktualisieren Sie dies entsprechend Ihrer URL-Struktur
        #url = "https://186.2.175.5/serie/stream/the-witcher/staffel-2/episode-1"
        global actual_episode
        actual_episode = i
        url = f"https://186.2.175.5/serie/stream/{name}/staffel-{staffel}/episode-{i}"
        print("Die URL ist:", url)
        open_seit(url)

if __name__ == "__main__":
    getInfo()
