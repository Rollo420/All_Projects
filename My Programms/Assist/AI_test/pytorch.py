import torch 
import torch.nn as nn 
import  torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim  

class MeinNetz(nn.Module):
    def __init__(self):
        super(MeinNetz, self).__init__()
        self.lin1 = nn.Linear(10, 10)
        self.lin2 = nn.Linear(10, 10)

    def forward( self, x):
        x = F.relu(self.lin1(x))
        x = self.lin2(x)

        return x

    def num_flat_Features(self, x):
        size = x.size()[1:]
        num = 1
        for i in size:
            num *= i

        return num

netz = MeinNetz()

if torch.cuda.is_available():
    dev = "cuda:0"
else: 
    dev = "cpu"
netz = netz.cuda(torch.device(dev))

for i in range(100):
    x = [1,0,0,0,1,0,0,0,1,1]
    input = Variable(torch.Tensor([x for  _ in range(10)]))
    input = input.cuda()

    out = netz(input)

    x = [0,1,1,1,0,1,1,1,0,0]
    target = Variable(torch.Tensor([x for _ in range(10)]))
    target = target.cuda()
    criterion = nn.MSELoss()
    loss = criterion(out, target)
    print(loss, f"in epoche {i}")

    netz.zero_grad()
    loss.backward()
    optimizer = optim.SGD(netz.parameters(), lr = 0.017)
    optimizer.step()