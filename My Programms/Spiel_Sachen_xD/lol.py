import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Tikok
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

from net_weazy.watcher import get_file_name


class KaisCrackstein:

    def __init__(self, headless=False):
        # Variablen
        self.username = 'Redicolus@proton.me'
        self.password = 'Quad2015!!'
        self.page           = 'https://www.instagram.com/'
        self.chrome_options = None
        self.failed_videos  = None
        self.submit_Button  = None
        self.input_username = None
        self.input_pass     = None
        self.cookies        = None
        self.auth           = None
        self.Disc           = f'{get_file_name(file_path)} \n #reddit #askreddit #askmen #reddit #minecraftparkour #fy'
        

        # Chrome-Optionen für headless-Betrieb
        self.chrome_options = webdriver.ChromeOptions()
        if headless:
            self.chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(self.page)
        self.driver.implicitly_wait(5)

    def upload_video(self, video_info: list):

        self.auth = AuthBackend(cookies=r'C:/Users/weazy/Desktop/Reddit/RedditVideoMakerBot/net_weazy/cookies.txt')
        self.failed_videos = upload_videos(videos=video_info, auth=self.auth, browser='chrome', headless=self.chrome_options)

        for video in self.failed_videos: # each input video object which failed
            print(f"{video['video']} with description '{video['description']}' failed")


    def find_My_element(self, css_path: str):
        # Findet das Element anhand des angegebenen CSS-Selectors
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_path))
        )
        return element
    
    def click_my_element(self, css_path):
        self.submit_Button = self.find_My_element(css_path)
        self.submit_Button.click()


    def login(self):
        # Klickt auf den Cookie-Banner, wenn vorhanden
        try:
            cookies = self.find_My_element("button._a9--._ap36._a9_0")
            cookies.click()
        except Exception as e:
            pass

        time.sleep(3)

        # Benutzername eingeben
        self.input_username = self.find_My_element('div._ab32:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
        self.input_username.clear()
        self.input_username.send_keys(self.username)

        # Passwort eingeben
        self.input_pass = self.find_My_element('div._ab32:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
        self.input_pass.clear()
        self.input_pass.send_keys(self.password)

        # Anmelden klicken
        submit = self.find_My_element('._acap')
        submit.click()

    
    def insta_upload(self, file_path):

        try:
            # Submit new Video
            self.click_my_element('div.x1iyjqo2:nth-child(2) > div:nth-child(7) > div:nth-child(1)')
            """ submit_video = self.find_My_element('div.x1iyjqo2:nth-child(2) > div:nth-child(7) > div:nth-child(1)')
            submit_video.click()"""

            # Submit upload file_push button
            self.click_my_element('button._acan:nth-child(1)')

            # Locate the file input element
            file_input = self.find_My_element('input[type="file"]')
            # Upload the file by sending the file path to the input element
            file_input.send_keys(file_path)

            self.click_my_element('body > div.x1n2onr6.xzkaem6 > div:nth-child(2) > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._a9-z > div > div.x78zum5.x1q0g3np.xdko459 > button')

            self.click_my_element('body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div')

            self.click_my_element('body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div')

            self.input_pass = self.find_My_element('body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div.x15wfb8v.x3aagtl.x6ql1ns.x78zum5.xdl72j9.x1iyjqo2.xs83m0k.x13vbajr.x1ue5u6n > div.xhk4uv.x26u7qi.xy80clv.x9f619.x78zum5.x1n2onr6.x1f4304s > div > div > div > div._ac2p > div:nth-child(2) > div > div.x6s0dn4.x78zum5.x1n2onr6.xh8yej3 > div > p > span')
            self.input_pass.clear()
            self.input_pass.send_keys(self.Disc)

            
            
            return True
        
        except RuntimeError:
            return False
        
    def close_browser(self):
        self.driver.quit()


if __name__ == '__main__':
    # Beispiel für die Verwendung der Klasse mit headless=True
    username = 'Redicolus@proton.me'
    password = 'Quad2015!!'
    path = r"C:\Users\vossj\Downloads\QpJEr3RHGY\bbswitzer-parkour.mp4"
    
    test = input("True or False? (y/n)").lower()
    if test == 'y':
        bot = KaisCrackstein(headless=True)
    elif test == 'n':
        bot = KaisCrackstein(headless=False)


    bot.login()
    bot.insta_upload(path)

    time.sleep(500)
