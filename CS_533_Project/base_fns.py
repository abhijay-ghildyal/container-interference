from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import networks_basic as networks
import os
import time

def train(config, model, device, train_loader, optimizer, epoch, log_interval, logging):
    
    iterations = 100
    model.train()
    epochStartTime = time.time()
    for batch_idx, (data, target) in enumerate(train_loader):
        batchStartTime = time.time()
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            # print('Train Epoch: {} [{:06d}/{} ({:.0f}%)]\tLoss: {:.6f}\tBatch Time:{:.4f}'.format(
            #     epoch, batch_idx * len(data), len(train_loader.dataset),
            #     100. * batch_idx / len(train_loader), loss.item(), time.time()-batchStartTime))
            logging.info('Docker: {}, Train Epoch: {} [{:06d}/{} ({:.0f}%)]\tLoss: {:.6f}\tBatch Time:{:.4f}'.format(config['docker_name'],
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item(), time.time()-batchStartTime))

        if batch_idx > iterations:
            break

    print('Epoch Time:{}'.format( time.time()-epochStartTime))

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def save_network(network, path, network_label, epoch_label):
        save_filename = '%s_net_%s.pth' % (epoch_label, network_label)
        save_path = os.path.join(path, save_filename)
        torch.save(network.state_dict(), save_path)

def load_network(network, path, network_label, epoch_label):
    save_filename = '%s_net_%s.pth' % (epoch_label, network_label)
    save_path = os.path.join(self.save_dir, save_filename)
    print('Loading network from %s'%save_path)
    network.load_state_dict(torch.load(save_path))  
