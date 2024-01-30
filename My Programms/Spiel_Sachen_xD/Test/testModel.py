import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence




# Testen des Modells
test_befehl = "Mach das Licht an"
test_seq = torch.tensor([word_to_idx[word] for word in test_befehl.split()]).unsqueeze(0)

# Laden des gespeicherten Modells
geladenes_modell = BefehlsModell(vocab_size, embedding_dim, hidden_dim, output_dim)
geladenes_modell.load_state_dict(torch.load('befehls_modell.pth'))
geladenes_modell.eval()  # Modell in den Evaluationsmodus versetzen

# Vorhersage machen
predicted_label = geladenes_modell(test_seq)
_, predicted_action_index = torch.max(predicted_label, 1)

# Aktion herausfinden
predicted_action = aktionen[predicted_action_index.item()]

print(f"Befehl: {test_befehl}")
print(f"Vorhergesagte Aktion: {predicted_action}")