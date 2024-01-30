import torch
import torchvision
from torchvision import transforms
from PIL import Image
import os 
import random
import torch.optim as optim
from torch.autograd import Variabel
import torch.nn.functional as F

#Taget: isCat, isDog
normalize = transforms.Normalize(
    mean = [0.485, 0.456, 0.406],
    std = [0.299, 0.224, 0.225]
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
files = os.listdir('CatDog\\train\\train\\')

for i in range(len(os.listdir('CatDog\\train\\train\\'))):
    f = random.choice(files)
    files.remove(f)

    img = Image.open(f"CatDog\\train\\train\\" + f)
    img_tensor = transform(img)
    train_data_list.append(img_tensor)

    isCat = 1 if 'cat' in f else 0
    isDog = 1 if 'dog' in f else 0
    target = [isCat, isDog]
    target_list.append(target)
    

    if len(train_data_list) >= 64:
       train_data.append((torch.stack(train_data_list), target_list))
       train_data_list = []
       break

print(train_data)


optimizer = optim.Adam(model.parameters(), lm=0.01)
def train(epoch):
    model.train()
    batch_id = 0

    for data, target in train_data:
        data = data.cuda()
        target = torch.Tensor(target).cuda()
        target = Variabel(target)

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
    for epoch in range(1.30):
        train(epoch)