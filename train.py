import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

DATA_PATH = './data/'  # default data directory
DEVICE = 'cpu'  # device on which to run the net

# load the dataset
def get_data():
    dataset = torchvision.datasets.ImageFolder(root=DATA_PATH, transform=transforms.ToTensor())
    loader = torch.utils.data.DataLoader(dataset, batch_size=128, shuffle=True, num_workers=2)
    return loader

class SoftmaxModel(nn.Module):
    def __init__(self, inputs=128*128*3, outputs=13):
        super(SoftmaxModel, self).__init__()
        self.fc1 = nn.Linear(inputs, outputs)

    def forward(self, x):
        x = torch.flatten(x, 1) # turn list of images into list of vectors
        x = self.fc1(x)
        return x        # return unnormalized probabilities
    
def train(net, dataloader, epochs=1, lr=0.01, momentum=0.9, decay=0.0005, verbose=1):
    net.to(DEVICE)
    losses = []
    criterion = nn.CrossEntropyLoss() # softmax + negative log likelihood
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=momentum, weight_decay=decay)
    for epoch in range(epochs):
        sum_loss = 0.0
        for i, batch in enumerate(dataloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = batch[0].to(DEVICE), batch[1].to(DEVICE)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize 
            outputs = net(inputs) # forward pass
            loss = criterion(outputs, labels) # calculating loss
            loss.backward()  # autograd magic, computes all the partial derivatives
            optimizer.step() # takes a step in negative gradient direction

            # print statistics
            losses.append(loss.item())
            sum_loss += loss.item()
            if verbose:
                print('[%d, %5d] loss: %.3f' %
                    (epoch + 1, i + 1, sum_loss / 100))
            sum_loss = 0.0

    # save network state and return
    torch.save(net, './net.pkl')
    return losses

# train the model
if __name__ == '__main__':
    net = SoftmaxModel()
    losses = train(net, get_data(), epochs=60)
    plt.plot(losses)