import torch
import torch.nn as nn
import gym

# Definieren Sie das DQN-Modell
class DQN(nn.Module):
    def __init__(self, inputs, outputs):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(inputs, 128)
        self.fc2 = nn.Linear(128, outputs)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# Erstellen Sie die Umgebung (zum Beispiel 'Snake-v0')
env = gym.make('Snake-v0')

# Erhalten Sie die Anzahl der Aktionen und Beobachtungen von der Umgebung
n_actions = env.action_space.n
n_observations = env.observation_space.shape[0]

# Erstellen Sie das DQN-Modell
model = DQN(n_observations, n_actions)

# Wählen Sie den Optimierer und die Verlustfunktion
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()

# Führen Sie eine Episode der Umgebung aus
state = env.reset()
for t in range(1000):
    # Wählen Sie eine Aktion
    state_tensor = torch.FloatTensor(state)
    q_values = model(state_tensor)
    _, action = q_values.max(0)
    action = action.item()

    # Führen Sie die Aktion aus und erhalten Sie die nächste Beobachtung und Belohnung
    next_state, reward, done, _ = env.step(action)
    next_state = torch.FloatTensor(next_state)

    # Aktualisieren Sie den Zustand
    state = next_state

    # Beenden Sie die Episode, wenn sie abgeschlossen ist
    if done:
        break
