from datetime import datetime
import os
import mysql.connector

file_path = r'G:\My Programms\Spiel_Sachen_xD\DiscordBot\schedule.txt'

def get_Current_day():
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

def read_file():

    try:
        # TXT-Datei öffnen und den Inhalt einlesen
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Den eingelesenen Inhalt ausgeben
        print(f'Inhalt der TXT-Datei ({file_path}):\n{file_content}')

        return file_content

    except FileNotFoundError:
        print(f'Die Datei "{file_path}" wurde nicht gefunden.')

    except Exception as e:
        print(f'Ein Fehler ist aufgetreten: {e}')



def write_file(content : str):

    content_in_file = read_file()
    current_day, current_date = get_Current_day()

    print(current_day)

    if current_day == "Monday":
        content = f"Montag {current_date}: {content}"

    elif current_day == "Tuesday":
        content = f'Dienstag {current_date}: {content}'

    elif current_day == "Wednesday":
        content = f'Mittwoch {current_date}: {content}'

    elif current_day == "Thursday":
        content = f'Donnerstag {current_date}: {content}'

    elif current_day == "Friday":
        content = f'Freitag {current_date}: {content}'

    with open(file_path, 'w') as file:
        file.write(f'{content_in_file + content}\n\n')


import mysql.connector
from datetime import datetime

def Datenbank():
    # Verbindung zur MySQL-Datenbank herstellen
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='berichtsheft'
    )

    # Ein Cursor-Objekt erstellen
    cursor = conn.cursor()

    # Funktionen, die Sie bereits haben (angenommen)
    content_in_file = read_file()
    current_day, current_date = get_Current_day()

    # Eine Tabelle erstellen, falls sie noch nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Add_by_User INT,
            content TEXT,
            create_on_Date DATE
        )
    ''')

    # Daten einfügen
    insert_query = '''
        INSERT INTO content (Add_by_User, content, create_on_Date)
        VALUES (%s, %s, %s)
    '''

    update_query = '''
    UPDATE content SET content="noch mal ein test" WHERE Add_by_User=1
    '''

    # Passen Sie die Werte an, je nachdem, was Sie für 'Add_by_User' und 'content' haben
    user_id = 1  # Beispielwert für 'Add_by_User'
    content = 'Ihr langer Text hier'  # Beispielwert für 'content'


    # Daten einfügen
    cursor.execute(update_query)

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()


# Funktion aufrufen
Datenbank()





if __name__ == '__main__':
    while True:
        userinput = input("Was Haben sie Heute Gemacht:\n")
        write_file(userinput)

        Datenbank()

        print("in der datei steht:\n", read_file())


