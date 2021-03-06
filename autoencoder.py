"""
In the task below you will have to build your own autoencoder neural network
model.

WE've already defined a model class for your AutoEncoder, and the tests
that your code has to pass. All you have to do is mainly fill the lines 39-40, 83-85. DO NOT USE CONVOLUTIONAL LAYERS
"""
import os
import torch
import argparse
import numpy as np
import torch.utils.data

from torch import nn, optim
from torch.autograd import Variable
from torchvision import datasets, transforms
from torchvision.utils import save_image


class AutoEncoder(nn.Module):
    def __init__(self, inp_size, hid_size):
        super(AutoEncoder, self).__init__()
        """
        Here you should define layers of your autoencoder
        Please note, if a layer has trainable parameters, it should be nn.Linear.
        ## !! CONVOLUTIONAL LAYERS CAN NOT BE HERE !! ##
        However, you can use any noise inducing layers, e.g. Dropout.
        Your network must not have more than six layers with trainable parameters.
        :param inp_size: integer, dimension of the input object
        :param hid_size: integer, dimension of the hidden representation
        """
        self.inp_size = inp_size
        self.hid_size = hid_size

        ################################################################
        # TODO:  Enter your code below!

        # Given above build encoder and decoder networks
        self.encoder =
        self.decoder =

    def param_reg_L1(self):
        """
        Applies regularisation to model parameters
        """

        # TODO:  Enter your code here!

        return

    def encode(self, x):
        """
        Encodes objects to hidden representations (E: R^inp_size -> R^hid_size)
        :param x: inputs, Variable of shape (batch_size, inp_size)
        :return:  hidden represenation of the objects, Variable of shape (batch_size, hid_size)
        """
        return self.encoder(x)

    def decode(self, h):
        """
        Decodes objects from hidden representations (D: R^hid_size -> R^inp_size)
        :param h: hidden represenatations, Variable of shape (batch_size, hid_size)
        :return:  reconstructed objects, Variable of shape (batch_size, inp_size)
        """
        return self.decoder(h)

    def forward(self, x):
        """
        Encodes inputs to hidden representations and decodes back.
        x: inputs, Variable of shape (batch_size, inp_size)
        return: reconstructed objects, Variable of shape (batch_size, inp_size)
        """
        return self.decode(self.encode(x))

    def loss_function(self, recon_x, x):
        """
        Calculates the loss function.
        :params recon_x: reconstructed object, Variable of shape (batch_size, inp_size)
        :params x: original object, Variable of shape (batch_size, inp_size)
        :return: loss
        """

        # TODO:  Enter your code here!

        return loss + reg_loss

def train(model, optimizer, train_loader, test_loader):
    for epoch in range(10):
        model.train()
        train_loss, test_loss = 0, 0
        for data, _ in train_loader:
            data = Variable(data).view(-1, 784)
            x_rec = model(data)
            loss = model.loss_function(x_rec, data)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        print('=> Epoch: %s Average loss: %.3f' % (epoch, train_loss / len(train_loader.dataset)))

        with torch.no_grad():
            model.eval()
            for data, _ in test_loader:
                data = Variable(data).view(-1, 784)
                x_rec = model(data)
                test_loss += model.loss_function(x_rec, data).item()

        test_loss /= len(test_loader.dataset)
        print('=> Test set loss: %.3f' % test_loss)

        n = min(data.size(0), 8)
        comparison = torch.cat([data.view(-1, 1, 28, 28)[:n], x_rec.view(-1, 1, 28, 28)[:n]])
        if not os.path.exists('./pics'): os.makedirs('./pics')
        save_image(comparison.data.cpu(), 'pics/reconstruction_' + str(epoch) + '.png', nrow=n)
    return model


def test_work():
    print('Start test')
    get_loader = lambda train: torch.utils.data.DataLoader(
        datasets.MNIST('./data', train=train, download=True, transform=transforms.ToTensor()),
        batch_size=50, shuffle=True)
    train_loader, test_loader = get_loader(True), get_loader(False)

    try:
        model = AutoEncoder(inp_size=784, hid_size=20)
        optimizer = optim.Adam(model.parameters(), lr=1e-3)
    except Exception:
        assert False, 'Error during model creation'
        return

    try:
        model = train(model, optimizer, train_loader, test_loader)
    except Exception:
        assert False, 'Error during training'
        return

    test_x = Variable(torch.randn(1, 784))
    rec_x, hid_x = model(test_x), model.encode(test_x)
    submodules = {**dict(model.decoder.named_children()), **dict(model.encoder.named_children())}
    layers_with_params = np.unique(['.'.join(n.split('.')[:-1]) for n, _ in model.named_parameters()])
    assert (hid_x.dim() == 2) and (hid_x.size(1) == 20),  'Hidden representation size must be equal to 20'
    assert (rec_x.dim() == 2) and (rec_x.size(1) == 784), 'Reconstruction size must be equal to 784'
    assert len(layers_with_params) <= 6, 'The model must have no more than 6 layers '
    assert np.all(np.concatenate([list(p.shape) for p in model.parameters()]) <= 800), 'All hidden sizes must be less than 800'
    print('Success!????')

if __name__ == '__main__':
    test_work()
