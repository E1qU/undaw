#!/usr/bin/env python
# -*- coding: utf-8 -*-

from torch import nn
from torch.nn import functional

__author__ = 'Konstantinos Drossos - Tampere University'
__docformat__ = 'reStructuredText'
__all__ = ['ModelAUDASC']


class ModelAUDASC(nn.Module):
    """The model M that is used in the AUDASC method.

    The code is from `the online GitHub repo of the AUDASC \
    method \
    <https://github.com/shayangharib/AUDASC/blob/master/modules/model.py>`_.

    The code has to be as in the online repo, otherwise the \
    saved states will not load by the default PyTorch method for \
    loading the states of a model.

    This class is used only for using the pre-trained model \
    by the AUDASC method.
    """

    def __init__(self):
        """Initialization of the model M.
        """
        super(ModelAUDASC, self).__init__()
        self.cnn_1 = nn.Conv2d(
            in_channels=1, out_channels=48,
            kernel_size=(11, 11), stride=(2, 3), padding=5
        )
        self.cnn_2 = nn.Conv2d(
            in_channels=48, out_channels=128,
            kernel_size=5, stride=(2, 3), padding=2
        )
        self.cnn_3 = nn.Conv2d(
            in_channels=128, out_channels=192,
            kernel_size=3, stride=1, padding=1
        )
        self.cnn_4 = nn.Conv2d(
            in_channels=192, out_channels=192,
            kernel_size=3, stride=1, padding=1
        )
        self.cnn_5 = nn.Conv2d(
            in_channels=192, out_channels=128,
            kernel_size=3, stride=1, padding=0
        )
        self.max_pool_1 = nn.MaxPool2d(
            kernel_size=3, stride=(1, 2)
        )
        self.max_pool_2 = nn.MaxPool2d(
            kernel_size=3, stride=(2, 2)
        )
        self.max_pool_3 = nn.MaxPool2d(
            kernel_size=3, stride=(1, 2)
        )

        self.bn_1 = nn.BatchNorm2d(48)
        self.bn_2 = nn.BatchNorm2d(128)
        self.bn_3 = nn.BatchNorm2d(128)

    def forward(self, x):
        """The forward pass of the model.

        :param x: The input.
        :type x: torch.Tensor
        :return: The output of the model.
        :rtype: torch.Tensor
        """
        output = self.bn_1(self.max_pool_1(functional.relu(self.cnn_1(x))))
        output = self.bn_2(self.max_pool_2(functional.relu(self.cnn_2(output))))

        output = functional.relu(self.cnn_3(output))
        output = functional.relu(self.cnn_4(output))
        output = self.bn_3(self.max_pool_3(functional.relu(self.cnn_5(output))))

        return output

# EOF
