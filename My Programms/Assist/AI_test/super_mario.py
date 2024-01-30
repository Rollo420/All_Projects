import torch
import torch.nn as nn
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
import numpy as np

# Erstellen Sie das DQN-Modell
class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.fc4 = nn.Linear(7 * 7 * 64, 512)
        self.fc5 = nn.Linear(512, len(SIMPLE_MOVEMENT))

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.relu(self.conv3(x))
        x = nn.functional.relu(self.fc4(x.view(x.size(0), -1)))
        return self.fc5(x)

# Erstellen Sie die Super Mario Bros-Umgebung
env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# Erstellen Sie das DQN-Modell
model = DQN()

# Führen Sie eine Aktion in der Umgebung aus und erhalten Sie das nächste Bild
state = env.reset()
observation, reward, done, info = env.step(env.action_space.sample())

# Verarbeiten Sie das Bild und geben Sie es in das Modell ein
state = np.transpose(state, (2, 0, 1))
state = np.ascontiguousarray(state, dtype=np.float32) / 255
state = torch.from_numpy(state)
state = state.unsqueeze(0)
q_values = model(state)
