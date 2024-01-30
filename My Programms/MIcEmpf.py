import pyaudio
import audioop

# Standard-Initialisierung von PyAudio
p = pyaudio.PyAudio()

# Index des zu verwendenden Geräts finden
device_index = None
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if dev_info["name"] == "AT2020USB+":
        device_index = i
        break

if device_index is None:
    print("Das Gerät wurde nicht gefunden")
    exit()

# Konfigurieren des Streams als Ausgangsstrom
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,
                output=True, input_device_index=device_index)

# Hier können Sie Ihre gewünschte Empfindlichkeit einstellen
target_volume = 0.8

while True:
    # Audio vom Stream abrufen
    data = stream.read(1024)

    # Berechnen Sie die Lautstärke des Audios
    rms = audioop.rms(data, 2)
    volume = rms / 32768.0

    # Skalieren Sie das Audio auf die gewünschte Lautstärke
    scaled_data = audioop.mul(data, 2, min(target_volume / volume, 1.0))

    # Schreiben Sie das skalierte Audio zurück in den Stream
    stream.write(scaled_data)

# Stream und PyAudio schließen
stream.stop_stream()
stream.close()
p.terminate()
