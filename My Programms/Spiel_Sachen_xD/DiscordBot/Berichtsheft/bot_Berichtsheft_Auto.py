from typing import Optional
import discord
from discord.ext import commands
from discord.ui import View, Button, button

from datetime import datetime
import os

from db_funktions import Datenbank

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

db = Datenbank()

class ColorButtons(View):
    def __init__(self):
        super().__init__()
        self.selected_color = None

    @button(label="Red", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Red"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)

    @button(label="Green", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Green"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)

    @button(label="Blue", style=discord.ButtonStyle.primary)
    async def blue_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Blue"
        await interaction.message.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)
    
    @button(label="Funktion", style=discord.ButtonStyle.secondary)
    async def funk_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "noch was testen"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=False)


class Control():
        
    def __init__(self, headless=True):

        # Variablen
        self.username = ''
        self.password = ''
        self.page     = 'https://www.instagram.com/'
        self.file_path = r'G:\My Programms\Spiel_Sachen_xD\DiscordBot\schedule.txt'

        # Chrome-Optionen für headless-Betrieb
        self.chrome_options = webdriver.ChromeOptions()
        if headless:
            self.chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(self.page)
        self.driver.implicitly_wait(2)

    def get_Current_day(self):
        # Aktuelles Datum und Uhrzeit abrufen
        current_datetime = datetime.now()

        # Wochentag als Text (z.B., "Montag", "Dienstag", usw.) im deutschen Format
        current_day = current_datetime.strftime('%A')

        # Datum als Text im deutschen Format (z.B., "31.01.2023")
        current_date = current_datetime.strftime('%d.%m.%Y')

        # Ausgabe des deutschen Wochentags und des Datums
        print(f'Aktueller Wochentag: {current_day}')
        print(f'Aktuelles Datum: {current_date}')

        return current_day, current_date

    def read_file(self):

        try:
            # TXT-Datei öffnen und den Inhalt einlesen
            with open(self.file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # Den eingelesenen Inhalt ausgeben
            print(f'Inhalt der TXT-Datei ({self.file_path}):\n{file_content}')

            return file_content

        except FileNotFoundError:
            print(f'Die Datei "{self.file_path}" wurde nicht gefunden.')

        except Exception as e:
            print(f'Ein Fehler ist aufgetreten: {e}')


    async def write_file(self, discordUserID ,content : str):

        current_day, current_date = self.get_Current_day()

        print(current_day)

        first_content = await db.select_all(discordUserID)

        second_content = first_content + content

        if current_day == "Monday":
            content = f"Montag {current_date}: {content}"

        elif current_day == "Tuesday":
            content = f'Dienstag {current_date}: {content}'

        elif current_day == "Wednesday":
            content = f'Mittwoch {current_date}: {content}'

        elif current_day == "Thursday":
            content = f'Donnerstag {current_date}: {second_content}'
            print("Second content: ", second_content)

        elif current_day == "Friday":
            content = f'Freitag {current_date}: {content}'

        await db.insert(discordUserID, content)


    def find_My_element(self, css_path: str):
        # Findet das Element anhand des angegebenen CSS-Selectors
        element = WebDriverWait(self.driver, 20).until(  # Increase the wait time to 20 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, css_path))
        )
        return element
    
    def click_my_element(self, css_path):
        try:
            self.submit_Button = self.find_My_element(css_path)
            self.submit_Button.click()

            return True
        except Exception as e:
            return False
        
    def login(self):

        try:
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
        except RuntimeError as e:
            print(f"Ich kontte mich nich anmelden!!!\nDer error ist: {e}")

    def upload_content_and_Save(self, mode="arbeit"):
        
        if mode == "arbeit":
            css_Skelet = "Hier Muss was Hin"
        
        elif mode == "schule":
            css_Skelet = "Hier Muss was Hin"
        
        self.login()

        # Content schreiben 
        self.write_content = self.find_My_element(css_Skelet)
        self.write_content.clear()
        self.write_content.send_keys(self.read_file())


        # Anmelden klicken
        submit = self.find_My_element('._acap')
        submit.click()

main = Control()

@bot.event
async def on_ready():
    print("Bot online!")


@bot.command()
async def btn(ctx: commands.Context):
    view = ColorButtons()
    await ctx.send("Choose a color:", view=view)


@bot.command()
async def write(ctx,*, content):
    discordUserID = ctx.author.id

    os.system('cls')
    #print(' '.join(c))

    await main.write_file(discordUserID,  content)#' '.join(args))
    await ctx.send(f"Der neue eintarg: {content} wurde hinzugefügt", delete_after=10)

@bot.command()
async def recentDay(ctx):

    discordUserID = ctx.author.id
    # Assuming output is a string containing the content you want to send
    output = await db.select_all(discordUserID)

    # Check if the content exceeds the Discord message limit
    if len(output) <= 2000:
        await ctx.send(f"Das aktuelle Berichtsheft:\n```{output}```")
    else:
        # Split the content into chunks of 2000 characters and send each chunk
        chunks = [output[i:i+2000] for i in range(0, len(output), 2000)]
        for chunk in chunks:
            await ctx.send(f"Das aktuelle Berichtsheft:\n```{chunk}```")

@bot.command()
async def test(ctx):

    """content = ' '.join(args)
    discordUserID = ctx.author.id
    print("content ist: ", content)
    await db.insert(discordUserID, content)"""
    lol = []
    a = 0
    for i in range(0,20000):
        print(lol)
        a+=i
        lol.append(a)


        if len(lol) <= 2000:
            await ctx.send(f"Das aktuelle Berichtsheft:\n```{lol}```")
        else:
            # Split the content into chunks of 2000 characters and send each chunk
            chunks = [lol[i:i+2000] for i in range(0, len(lol), 2000)]
            for chunk in chunks:
                await ctx.send(f"Das aktuelle Berichtsheft:\n```{chunk}```")

@bot.command()
async def update(ctx):

    db.update_test()

    await ctx.send(f'Die Daten wurden geupdatet', delete_after=10)


bot.run(TOKEN)
