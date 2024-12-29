import os
import numpy as np
import torch
import torchvision
from torch import nn
from pathlib import Path

from ..trainers import BTrainer
from ..utils import get_device
from ..model import BResNet18
from ..lr_schedulers import BWarmupDecayLR

def get_dataset(batch_size, saveDir):
    from torch.utils.data import random_split, DataLoader
    from torchvision import transforms

    os.makedirs(saveDir / "dataset", exist_ok=True)

    image_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    datasets = torchvision.datasets.MNIST(saveDir / "dataset", train=True, download=True, transform=image_transform)
    train_datasets, val_datasets = random_split(datasets, [55000, 5000])
    train_datasets = torch.utils.data.Subset(train_datasets, np.arange(1000))
    val_datasets = torch.utils.data.Subset(val_datasets, np.arange(1000))

    train_dataloader = DataLoader(train_datasets, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_datasets, batch_size=8, shuffle=False)

    return train_dataloader, val_dataloader

def mnist(saveDir):
    saveDir = Path(saveDir)
    os.makedirs(saveDir, exist_ok=True)
    #### 超参数 ####
    lr = 1e-4
    batch_size = 128
    epochs = 5
    device = get_device()

    #### 数据集 ####
    train_dataloader, val_dataloader = get_dataset(batch_size, saveDir)

    #### 模型 ####
    net = BResNet18()
    net.blk0 = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=64, kernel_size=7, stride=2, padding=3),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    )
    net.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    lr_scheduler = BWarmupDecayLR(optimizer, 5e-5, 3, 3)
    #### Trainer ####
    myTrainer = BTrainer(net, train_dataloader, val_dataloader, optimizer, criterion, device,
                         lrScheduler=lr_scheduler,isParallel=True)
    myTrainer.set_logger(logPath=saveDir / 'logawa.txt', mode='w')
    myTrainer.set_reload_by_loss(5, 10)
    #### 训练/测试 ####
    myTrainer.train_eval_s(epochs)

    #### 保存模型 ####
    myTrainer.save_best_checkpoint(saveDir / 'checkpoint/best_checkpoint.pth')

    myTrainer.calculate_model(dataloader=val_dataloader)
    myTrainer.load_model(saveDir / 'checkpoint/best_checkpoint.pth')
    myTrainer.calculate_model(dataloader=val_dataloader)

    #### 画图 ####
    myTrainer.draw(saveDir / 'checkpoint/latest_checkpoint.jpg', isShow=False)

if __name__ == '__main__':
    saveDir = '.'
    mnist(saveDir)