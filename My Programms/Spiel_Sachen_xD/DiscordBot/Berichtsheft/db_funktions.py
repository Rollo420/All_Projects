from datetime import datetime
import os
import mysql.connector

class Datenbank():
    def __init__(self) -> None:
        # Verbindung zur MySQL-Datenbank herstellen
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='berichtsheft'
        )
        
        # Ein Cursor-Objekt erstellen
        self.cursor = self.conn.cursor()

        # Eine Tabelle erstellen, falls sie noch nicht existiert
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Add_by_User INT,
                content TEXT,
                create_on_Date DATE
            )
        ''')
    
    def select_user(self, discordUserID):

        select_query = '''
            SELECT `userID` FROM `users` WHERE discordUserID=%s
        '''

        self.cursor.execute(select_query, (discordUserID,))
        result = self.cursor.fetchone()

        # Überprüfen Sie, ob ein Benutzer mit dem angegebenen Benutzernamen gefunden wurde
        if result:
            userID : int = result[0]
            print(userID)
            return userID
        else:
            return None

    async def select_all(self, discordUserID):

        select_query = '''
            SELECT C.content FROM `users` as U INNER JOIN content as C ON U.userID = C.Add_by_User
        '''

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        # Überprüfen Sie, ob ein Benutzer mit dem angegebenen Benutzernamen gefunden wurde
        if result:
            out_content = ' '.join(result[-1])
            print(out_content)
            return out_content
        else:
            return ''

    def update_test(self):

        update_query = 'UPDATE `content` SET `Add_by_User`=2 WHERE Add_by_User=1'

        # Daten einfügen
        self.cursor.execute(update_query)
        self.conn.commit()
        

    async def insert(self, discordUserID, content : str):

        # Daten einfügen
        insert_query = '''
            INSERT INTO content (Add_by_User, content)
            VALUES ( %s, %s)
        '''

        # Überprüfen, ob der Benutzer gefunden wurde
        print("userid ",discordUserID)
        user_id = self.select_user(discordUserID)
        print("useridsql", user_id)

        if user_id is not None:
            print(content)

            # Daten einfügen
            self.cursor.execute(insert_query, (user_id, content))
            self.conn.commit()

            
        else:
            print("Benutzer nicht gefunden.")
