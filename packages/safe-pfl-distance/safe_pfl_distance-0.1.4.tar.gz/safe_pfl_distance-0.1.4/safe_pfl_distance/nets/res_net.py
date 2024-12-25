import torch.nn as nn
import torchvision.models as models


class Net(
    nn.Module,
):
    def __init__(self):
        super(Net, self).__init__()

        self.resnet18 = models.resnet18(pretrained=False)

    def forward(self, x):
        out = self.resnet18(x)
        return out
