import speech_recognition as sr
import pyttsx3
import os
import re
import openai
import webbrowser
import requests
import json

# Erstellen Sie einen Spracherkennungs-Engine
recognizer = sr.Recognizer()

# Erstellen Sie einen Sprachsynthesizer
engine = pyttsx3.init()




def chat_with_gpt(prompt):
    # Setze deinen OpenAI API-Schlüssel hier ein
    openai.api_key = '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'

    response = openai.Completion.create(
        engine="text-davinci-002",  # Du kannst auch andere Engines verwenden
        prompt=prompt,
        max_tokens=1500
    )

    return response.choices[0].text.strip()



# Funktion zum Ausführen des Herunterfahrens nach einer bestimmten Zeit
def shutdown_after_minutes(minutes):
    os.system(f"shutdown /s /t {minutes * 60}")

# Funktion zum Ausführen des Herunterfahrens abbrechen
def shutdown_cancel():
    os.system("shutdown /a")

# Funktion zum Öffnen einer App
def open_app(app_name):
    if app_name == "task":
        os.system(f"start taskmgr")
    else:
        try:
            os.system(f"start {app_name}")
        except Exception as e:
            print(f"Fehler beim Öffnen der App: {e}")

# Funktion zum Ändern der Lautstärke des PCs
def change_volume(volume_level):
    os.system(f"vol {volume_level}")

# Funktion zum Ändern der Empfindlichkeit des Mikrofons
def change_mic_sensitivity(sensitivity_level):
    os.system(f"mic {sensitivity_level}")

# Funktion zum Extrahieren der Zeit aus dem Sprachbefehl
def extract_time_from_command(command):
    # Verwenden Sie reguläre Ausdrücke, um die Minuten zu extrahieren
    match = re.search(r'(\d+)\s*minuten', command)
    if match:
        minutes = int(match.group(1))
        return minutes
    else:
        return None

# Hauptfunktion zum Verarbeiten von Sprachbefehlen
def process_speech_command():
    with sr.Microphone() as source:
        print("Sagen Sie einen Befehl...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="de-DE").lower()
            print("Erkannter Befehl:", command)

            if "peter" in command:
                if   "herunterfahren" in command:
                    
                    minutes = extract_time_from_command(command)
                    if minutes is not None:
                        shutdown_after_minutes(minutes)
                elif "lautstärke"     in command:
                    volume_level = command.split("lautstärke")[1]
                    change_volume(volume_level)
                elif "abbrechen"      in command:
                    shutdown_cancel()
                elif "schließen"      in command:
                    exit()
                elif "öffne"          in command:
                    open_app(command.replace("öffne ", ""))
                elif "chat gpt"       in command:
                    # Beispielanfrage an ChatGPT
                    frage = command.replace("peter chat gpt ", "")

                    # ChatGPT um Antwort bitten
                    antwort = chat_with_gpt(frage)
                    print(antwort)

                    # Antwort in eine Datei schreiben
                    with open("antwort.txt", "w", encoding="utf-8") as file:
                        file.write(antwort)
 




        except sr.UnknownValueError:
            print("Konnte den Befehl nicht verstehen.")
        except sr.RequestError as e:
            print("Fehler bei der Spracherkennung: {0}".format(e))

# Sprachbefehle verarbeiten
while True:
    process_speech_command()
