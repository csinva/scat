'''AlexNet for CIFAR10. FC layers are removed. Paddings are adjusted.
Without BN, the start learning rate should be 0.01
(c) YANG, Wei 
'''
import torch
import torch.nn as nn
from .scatwave.scattering import Scattering



__all__ = ['scatfirst_fnum']


class ScatFirst_FNum(nn.Module):

    def __init__(self, num_classes=10):
        super(ScatFirst_FNum, self).__init__()
        self.J = 2
        self.N = 32
        self.L = 4
        self.scat = Scattering(M=32,N=32,J=self.J, L = self.L).cuda()
        print(len(self.scat.Psi))
        self.nfscat = (1 + self.L * self.J + self.L * self.L * self.J * (self.J - 1) / 2)
        print(self.nfscat*3)
        self.nspace = self.N / (2 ** self.J)

        self.features = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(self.nfscat*3, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Linear(256, num_classes)

    def forward(self, x):
        x = torch.autograd.Variable(self.scat(x.data), requires_grad = False)
        x = x.view(x.size(0), self.nfscat*3, self.nspace, self.nspace)
        #print("X2SHAPE")
        #print(x2.shape)
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def scatfirst_fnum(**kwargs):
    """AlexNet model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1404.5997>`_ paper.
    """
    model = ScatFirst_FNum(**kwargs)
    return model
