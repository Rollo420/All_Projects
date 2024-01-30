import os
import time
import torch
import torch.nn  as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable


path_train = os.path.dirname(__file__)


kwargs={'num_workers': 0, 'pin_memory': True} # wenn mit CUDA gearbeitet wird muss da noch eine worker hinzugefügt werden 
train_data = torch.utils.data.DataLoader(datasets.MNIST( path_train + '\data', train=True, download=True,
                                                    transform=transforms.Compose([transforms.ToTensor(),
                                                    transforms.Normalize((0.1307,), (0.3081,))])), #0.1307 0.3081
                                     batch_size=3000, shuffle=True, **kwargs)


test_data =  torch.utils.data.DataLoader(datasets.MNIST(path_train + '\data', train=False,
                                                    transform=transforms.Compose([transforms.ToTensor(),
                                                    transforms.Normalize((0.1307,), (0.3081,))])),
                                     batch_size=3000, shuffle=True, **kwargs)


class Netz(nn.Module):

    def __init__(self):
        super(Netz, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv_dropout = nn.Dropout2d(0.5)

        self.fc1 = nn.Linear(320, 60)
        self.fc2 = nn.Linear(60, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x,2)
        x = F.relu(x)

        x = self.conv2(x)
        x = self.conv_dropout(x)

        x = F.max_pool2d(x,2)
        x = F.relu(x)


        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))

        x = self.fc2(x)
        
        return F.log_softmax(x , dim=1)



model = Netz()  
model.cuda()


if os.path.isfile(path_train +'\Model\Handschrifterkennung_Train01.pt'):
    model = torch.load(path_train +'\Model\Handschrifterkennung_Train01.pt')
    print(model)
    print("Modle is loding...")
    time.sleep(2)
else:
    if os.path.exists(path_train+ "\Model"):
        pass
    else:
        os.mkdir(path_train +'\Model')




optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.8)

def train(epoch):
    model.train()

    for batch_id, (data, target) in enumerate(train_data):
        data = data.cuda()
        target = target.cuda()
        data = Variable(data)
        target = Variable(target)

        optimizer.zero_grad()

        out = model(data)
        criterion = F.nll_loss

        loss = criterion(out, target)
        loss.backward()

        torch.save(model.cuda(), path_train +'\Model\Handschrifterkennung_Train01.pt')

        optimizer.step()
        print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(epoch, batch_id * len(data), len(train_data.dataset),
                                                                       100. * batch_id / len(train_data), loss.item()))
        
def test():
    model.eval()

    loss = 0
    correct = 0

    for data, target in test_data:
        data = Variable(data.cuda(), volatile=True)
        target = Variable(target.cuda())

        out = model(data)
        loss += F.nll_loss(out, target, reduction='sum').item()  # Verwenden Sie 'reduction' anstelle von 'size_average'
        prediction = out.data.max(1, keepdim=True)[1]
        correct += prediction.eq(target.data.view_as(prediction)).cpu().sum()

    loss = loss / len(train_data.dataset)
    print("Durchschnitts Verlust:", loss, "\nGenauigkeit: ", 100*correct/len(test_data.dataset))





if __name__ == "__main__":
    for epoch in range(1,10):
        #train(epoch)
        test()