import os
import signal
import subprocess
import time
import psutil
import threading

# Befehle zum Starten der beiden Skripte
command_server = r'node .\src\\components\\Server\\server.js'
command_npm = 'npm start'

start_server_process = None  # Globale Variable, um den Server-Prozess zu speichern
start_npm_process = None  # Globale Variable, um den npm-Prozess zu speichern


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def start_server():
    global start_server_process
    start_server_process = run_command(command_server)


def start_npm():
    global start_npm_process
    start_npm_process = run_command(command_npm)


def kill_process(process):
    if process and process.poll() is None:
        try:
            # Unter Windows den Prozess mit psutil beenden
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            psutil.wait_procs([parent], timeout=5)
        except Exception as e:
            print(f"Error while terminating process: {e}")


def handle_user_input():
    while True:
        os.system('cls')
        command = int(input(f'Was möchten Sie machen?\n\n0. Start All\n' +                           
                            f'1. Start Server\n2. Start npm\n' +
                            f'3. Restart Server\n4. Restart npm\n' +
                            f'5. Stop Server\n6. Stop npm\n7. Exit\n> ').strip() or 0)

        if command == 0:
            start_server()
            start_npm()

        elif command == 1:
            start_server()
        
        elif command == 2:
            start_npm()
            
            
        elif command == 3:
            kill_process(start_server_process)
            time.sleep(3)
            start_server()

        elif command == 4:
            kill_process(start_npm_process)
            time.sleep(3)
            start_npm()
            

        elif command == 5:
            kill_process(start_server_process)

        elif command == 6:
            kill_process(start_npm_process)

        elif command == 7:
            kill_process(start_npm_process)
            kill_process(start_server_process)
            break


if __name__ == '__main__':    

    # Starte den Thread für die Benutzereingabe
    user_input_thread = threading.Thread(target=handle_user_input)
    user_input_thread.start()

    # Warte darauf, dass der Benutzereingabe-Thread beendet ist
    user_input_thread.join()

    print("Das Programm wurde beendet.")
