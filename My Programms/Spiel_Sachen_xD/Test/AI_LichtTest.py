import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

befehle = [
    "licht an",
    "licht aus",
    "licht Raum an",
    "licht Raum aus",
    "licht Farbe an",
    "licht Farbe aus",
    "licht Helligkeit an",
    "licht Helligkeit aus",
    "rollläden hoch",
    "rollläden runter",
    "rollläden Raum hoch",
    "rollläden Raum runter",
    "heizung an",
    "heizung aus",
    "heizung Raum an",
    "heizung Raum aus",
    "heizung Temperatur an",
    "heizung Temperatur aus",
    "kühlschrank an",
    "kühlschrank aus",
    "garage auf",
    "garage zu",
    "staubsauger an",
    "staubsauger aus",
    "staubsauger Raum an",
    "staubsauger Raum aus",
    "waschmaschine an",
    "waschmaschine aus",
    "waschmaschine Programm starten",
    "waschmaschine Programm abbrechen",
    "trockenmaschine an",
    "trockenmaschine aus",
    "trockenmaschine Programm starten",
    "trockenmaschine Programm abbrechen",
    "spülmaschine an",
    "spülmaschine aus",
    "spülmaschine Programm starten",
    "spülmaschine Programm abbrechen",
]
aktionen = [
    "Licht einschalten",
    "Licht ausschalten",
    "Licht im [Raum] einschalten",
    "Licht im [Raum] ausschalten",
    "Licht in [Farbe] einschalten",
    "Licht in [Farbe] ausschalten",
    "Licht auf [Helligkeit] setzen",
    "Licht auf [Helligkeit] setzen",
    "Rollläden hochfahren",
    "Rollläden runterfahren",
    "Rollläden im [Raum] hochfahren",
    "Rollläden im [Raum] runterfahren",
    "Heizung einschalten",
    "Heizung ausschalten",
    "Heizung im [Raum] einschalten",
    "Heizung im [Raum] ausschalten",
    "Heizung auf [Temperatur] setzen",
    "Heizung auf [Temperatur] setzen",
    "Kühlschrank einschalten",
    "Kühlschrank ausschalten",
    "Garage öffnen",
    "Garage schließen",
    "Staubsauger einschalten",
    "Staubsauger ausschalten",
    "Staubsauger im [Raum] einschalten",
    "Staubsauger im [Raum] ausschalten",
    "Waschmaschine starten",
    "Waschmaschine stoppen",
    "Waschmaschine mit [Programm] starten",
    "Waschmaschine mit [Programm] stoppen",
    "Trockenmaschine starten",
    "Trockenmaschine stoppen",
    "Trockenmaschine mit [Programm] starten",
    "Trockenmaschine mit [Programm] stoppen",
    "Spülmaschine starten",
    "Spülmaschine stoppen",
    "Spülmaschine mit [Programm] starten",
    "Spülmaschine mit [Programm] stoppen",
]


# Tokenizer für die Befehle
word_to_idx = {word: idx + 1 for idx, word in enumerate(set(" ".join(befehle).split()))}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}

# Befehle in Sequenzen umwandeln
input_sequences = [torch.tensor([word_to_idx[word] for word in befehl.split()]) for befehl in befehle]

# Padding für einheitliche Eingabeform
input_sequences = pad_sequence(input_sequences, batch_first=True)

# Aktionen in Sequenzen umwandeln
labels = torch.tensor([aktionen.index(a) for a in aktionen])

class BefehlsDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.labels[idx]

# Modell erstellen
class BefehlsModell(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(BefehlsModell, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.rnn(embedded)
        output = self.fc(output[:, -1, :])
        return output

# Hyperparameter
vocab_size = len(word_to_idx) + 1
embedding_dim = 16
hidden_dim = 32
output_dim = len(aktionen)
epochs = 100
lr = 0.001

# Modell, Verlustfunktion und Optimierer erstellen
befehls_modell = BefehlsModell(vocab_size, embedding_dim, hidden_dim, output_dim)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(befehls_modell.parameters(), lr=lr)

# Daten laden
dataset = BefehlsDataset(input_sequences, labels)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# Modell trainieren
for epoch in range(epochs):
    for inputs, labels in dataloader:
        optimizer.zero_grad()
        outputs = befehls_modell(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    
# Speichern des Modells
torch.save(befehls_modell.state_dict(), r'G:\My Programms\Spiel_Sachen_xD\Test\befehls_modell.pth')

while True:
    # Testen des Modells
    test_befehl = input("Was soll der befehl sein?\n")
    test_seq = torch.tensor([word_to_idx[word] for word in test_befehl.split()]).unsqueeze(0)

    # Vorhersage machen
    predicted_label = befehls_modell(test_seq)
    _, predicted_action_index = torch.max(predicted_label, 1)

    # Aktion herausfinden
    predicted_action = aktionen[predicted_action_index.item()]

    print(f"Befehl: {test_befehl}")
    print(f"Vorhergesagte Aktion: {predicted_action}")
