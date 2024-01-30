import torch
from torch import nn, optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os
import random

# Definieren Sie die Transformationen für die Trainings- und Testdaten
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Skaliert alle Bilder auf 64x64 Pixel
    transforms.ToTensor(),  # Konvertiert die Bilder in Tensoren
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalisiert die Bilder
])

# Laden Sie die Trainings- und Testdaten
train_data_path = 'G:/My Programms/Assist/AI_test/CatDog/train/train'
test_data_path = 'G:/My Programms/Assist/AI_test/CatDog/test'
train_data = datasets.ImageFolder(train_data_path, transform=transform)
test_data = datasets.ImageFolder(test_data_path, transform=transform)

# Erstellen Sie DataLoaders für die Trainings- und Testdaten
train_loader = nn.DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = nn.DataLoader(test_data, batch_size=64, shuffle=True)

# Definieren Sie das Modell
model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1),  # Eingang ist 3 Kanäle (RGB), Ausgang ist 16 Kanäle
    nn.ReLU(),
    nn.MaxPool2d(2, 2),  # Max-Pooling reduziert die Größe der Bilder um die Hälfte
    nn.Conv2d(16, 32, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2, 2),
    nn.Flatten(),  # Flacht die Bilder in einen Vektor ab
    nn.Linear(32*16*16, 256),  # Vollständig verbundene Schicht
    nn.ReLU(),
    nn.Linear(256, 2)  # Ausgangsschicht für 2 Klassen (Hunde und Katzen)
)

# Definieren Sie den Verlust und den Optimierer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

# Eine Liste zum Speichern der Verluste
losses = []

# Trainieren Sie das Modell
for epoch in range(10):  # Durchläuft die Daten 10 Mal
    for images, labels in train_loader:
        # Nullt die Gradienten
        optimizer.zero_grad()

        # Macht eine Vorhersage
        output = model(images)

        # Berechnet den Verlust
        loss = criterion(output, labels)

        # Fügt den Verlust zur Liste hinzu
        losses.append(loss.item())

        # Rückwärtspropagation
        loss.backward()

        # Aktualisiert die Gewichte
        optimizer.step()

    print(f'Epoch {epoch+1} completed')

# Zeigt ein Diagramm der Verluste
plt.plot(losses)
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.show()
