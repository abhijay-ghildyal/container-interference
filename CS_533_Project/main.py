from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import os
import networks_basic as networks
from base_fns import *

# import redis
import json
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logs/main.log', level=logging.INFO)

parser = argparse.ArgumentParser(description='used for getting config file name')
parser.add_argument('--configFileName', type=str, default='', help='config file name with path')
args = parser.parse_args()

with open(args.configFileName) as f:
  config = json.load(f)

use_cuda = not config['no_cuda'] and torch.cuda.is_available()
torch.manual_seed(config["seed"])
device = torch.device('cuda' if use_cuda else 'cpu')
kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

def main():

    if not os.path.isdir(os.path.join(config["model_path"], config["model_name"])):
    	os.mkdir(os.path.join( config["model_path"]
            , config["model_name"]))

    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=config["batch_size"], shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=False, transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=config["test_batch_size"], shuffle=True, **kwargs)

    model = networks.Net().to(device)

    if config["load_model"]:
    	load_network( model, config["model_path"], config["model_name"], config["load_at_epoch"])

    optimizer = optim.Adadelta(model.parameters(), lr=config["lr"])

    scheduler = StepLR(optimizer, step_size=1, gamma=config["gamma"])

    # r = redis.Redis(host='localhost', port=6379, db=0)
    # r.set('foo', str([args.modelName]))

    for epoch in range(1, config["epochs"]):
        train(config, model, device, train_loader, optimizer, epoch, config["log_interval"], logging)
        if config["save_model"]:
            save_network(model, config["model_path"], config["model_name"], epoch)
        test(model, device, test_loader)
        scheduler.step()

    # if args.save_model:
    #     torch.save(model.state_dict(), "mnist_cnn.pt")


if __name__ == '__main__':
    main()

# # for keybatch in r.scan_iter():
# #     r.delete(key)

