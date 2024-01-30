import torch
import torchvision
from torchvision import transforms
from PIL import Image
import os 
import random
import torch.optim as optim
from torch.autograd import Variable
from torch import nn, optim
import torch.nn.functional as F

# Überprüfen Sie, ob CUDA verfügbar ist und setzen Sie das Gerät entsprechend
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("The Device is:", device)

# Ziel: isCat, isDog
normalize = transforms.Normalize(
    mean = [0.485, 0.456, 0.406],
    std = [0.229, 0.224, 0.225]
)

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    normalize
])

train_data_list = []
train_data = []
target_list = []
files = os.listdir(r'CatDog/train/train')

for i in range(len(os.listdir(r'CatDog\\train\\train\\'))):
                                        
    f = random.choice(files)
    files.remove(f)

    img = Image.open(f"CatDog\\train\\train\\" + f)
    img_tensor = transform(img)
    train_data_list.append(img_tensor)

    isDog = 1 if 'dog' in f else 0
    target_list.append(isDog)
    

    if len(train_data_list) >= 128:
       train_data.append((torch.stack(train_data_list).to(device), torch.LongTensor(target_list).to(device)))
       train_data_list = []
       target_list = []

print(train_data)

# Definieren Sie das Modell
model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1),  # Eingang ist 3 Kanäle (RGB), Ausgang ist 16 Kanäle
    nn.ReLU(),
    nn.MaxPool2d(2, 2),  # Max-Pooling reduziert die Größe der Bilder um die Hälfte
    nn.Conv2d(16, 32, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2, 2),
    nn.Flatten(),  # Flacht die Bilder in einen Vektor ab
    nn.Linear(32*64*64, 256),  # Vollständig verbundene Schicht
    nn.ReLU(),
    nn.Linear(256, 2),  # Ausgangsschicht für 2 Klassen (Hunde und Katzen)
    nn.LogSoftmax(dim=1)
).to(device)

optimizer = optim.Adam(model.parameters(), lr=0.01)
def train(epoch):
    model.train()
    batch_id = 0

    for data, target in train_data:
        data = data.to(device)
        target = target.to(device)
        target = Variable(target)

        optimizer.zero_grad()
        out = model(data)
        criterion = F.nll_loss

        loss = criterion(out, target)
        loss.backward()

        optimizer.step()

        print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(epoch, batch_id * len(data), len(train_data),
                                                                       100. * batch_id / len(train_data), loss.item()))

        batch_id += 1


if __name__ == "__main__":
    for epoch in range(1, 30):
        train(epoch)
