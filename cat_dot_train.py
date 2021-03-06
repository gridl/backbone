import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from back import Bone, utils
from models.vgg import vgg11
from datasets import cat_dog

data_dir = 'train'
num_classes = 2
batch_size = 32
epochs_count = 20
num_workers = 8

datasets = cat_dog.get_datasets(data_dir)
model = vgg11(num_classes, batch_norm=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
scheduler = StepLR(optimizer, step_size=10, gamma=0.5)
criterion = nn.CrossEntropyLoss()

backbone = Bone(model,
                datasets,
                criterion,
                optimizer,
                scheduler,
                scheduler_after_ep=False,
                metric_fn=utils.accuracy_metric,
                metric_increase=True,
                batch_size=batch_size,
                num_workers=num_workers)

backbone.fit(epochs_count)
