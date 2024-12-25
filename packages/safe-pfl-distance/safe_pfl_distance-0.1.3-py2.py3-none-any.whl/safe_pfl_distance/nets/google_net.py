import torch.nn as nn
import torchvision.models as models


class Net(
    nn.Module,
):
    def __init__(self, num_classes=10):
        super(Net, self).__init__()
        self.googlenet = models.googlenet_v2(pretrained=False)
        self.googlenet.classifier[1] = nn.Linear(
            self.googlenet.last_channel, num_classes
        )

    def forward(self, x):
        out = self.googlenet(x)
        return out
