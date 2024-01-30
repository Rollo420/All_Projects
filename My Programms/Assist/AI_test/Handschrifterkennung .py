import os
import time
import torch
import torch.nn  as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable


path_train = os.path.dirname(__file__)

kwargs={} # wenn mit CUDA gearbeitet wird muss da noch eine worker hinzugefügt werden 
train_data = torch.utils.data.DataLoader(datasets.MNIST( path_train + '\data', train=True, download=True,
                                                    transform=transforms.Compose([transforms.ToTensor(),
                                                    transforms.Normalize((0.1307,), (0.3081,))])), #0.1307 0.3081
                                     batch_size=128, shuffle=True, **kwargs)


test_data =  torch.utils.data.DataLoader(datasets.MNIST(path_train + '\data', train=False,
                                                    transform=transforms.Compose([transforms.ToTensor(),
                                                    transforms.Normalize((0.1307,), (0.3081,))])),
                                     batch_size=128, shuffle=True, **kwargs)



class Netz(nn.Module):
    def __init__(self):
        super(Netz, self).__init__()
        self.conv1 = nn.Conv2d(1,20, kernel_size=5)
        self.conv2 = nn.Conv2d(20, 30, kernel_size=5)
        self.conv_dropout = nn.Dropout2d()
        
        self.fc1 = nn.Linear(320, 60)
        self.fc2 = nn.Linear(60, 10)
    
    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        
        x = self.conv2(x)
        x = self.conv_dropout(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = x.view(-1,320)
        
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return F.log_softmax(x, dim=1)
#C:\Projekte\Schulungen\python-schulung\Train_data.pt
#C:\Projekte\Schulungen\python-schulung\Assistent\AI\Handschrifterkennung .py
model = Netz()
model = model.cuda()

if os.path.exists(path_train +'\Model\Handschrifterkennung_Train.pt'):
    model = torch.load(path_train +'\Model\Handschrifterkennung_Train.pt')
    print("Modle is loding...")
    time.sleep(2)
else:
    if os.path.exists(path_train+ "\Model"):
        pass
    else:
        os.mkdir(path_train +'\Model')
    
    
optimizer = optim.SGD(model.parameters(), lr= 0.5, momentum=0.8)

def train(epoch):
    model.train()
    
    for batch_id, (data, target) in enumerate(train_data):
        data = Variable(data)
        data = data.cuda()
        
        target = Variable(target)
        target = target.cuda()
        optimizer.zero_grad()
        
        out = model(data)
        
        criterion = F.nll_loss
        loss = criterion(out, target)
        loss.backward()
        optimizer.step()
        
        torch.save(model, path_train +'\Model\Handschrifterkennung_Train.pt')
        
        print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(epoch, batch_id * len(data), len(train_data.dataset),
                                                                       100. * batch_id / len(train_data), loss.item()))
        

def test():
    model.eval()
    loss = 0
    correct = 0
    
    for data, target in test_data:
        data = Variable(data, volatile=True)
        data = data.cuda()
        
        target = Variable(target)
        target = target.cuda()
        
        out = model(data)
        loss = F.nll_loss(out, target, size_average=False).item()
        prediction = out.data.max(1, keepdim=True)[1]
        
        loss = loss / len(test_data.dataset)
        
        correct += prediction.eq(target.data.view_as(prediction)).cpu().sum()
        print("Durchschnitts Verlust:", loss ,"\ngenauigkeit: ", 100.*correct/len(test_data.dataset))
        

"""if __name__ == "__main__":
    train(200)"""
    
for epoch in range(1,400):
    train(epoch)
    test()