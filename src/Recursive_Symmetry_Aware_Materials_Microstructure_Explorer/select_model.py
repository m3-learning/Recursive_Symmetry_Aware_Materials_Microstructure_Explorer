import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch import optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def select_model(data_loader, batch_size, images,
                 model_type='vgg', N_EPOCHS=5,
                 verbose=False):
    """
    :param data_loader: input data loader
    :type data_loader: torch.utils.data.DataLoader
    :param batch_size: number of data for everytime training
    :type batch_size: int
    :param images: same size of the input data
    :type images: numpy array
    :param model_type: set the model type for training
    :type model_type: string
    :param resnet_model_path: path of the resnet model
    :type resnet_model_path: string
    :param N_EPOCHS: number of epochs for autoencoder model training
    :type N_EPOCHS: int
    :param verbose: Does the program output information
    :type verbose: bool
    :return: training result
    :rtype: numpy arrray
    """

    if model_type == 'vgg' or model_type == 'both':
        vgg_model = torch.hub.load(
            'pytorch/vision:v0.6.0', 'vgg16', pretrained=True)
        vgg_model.classifier = nn.Sequential(
            *[vgg_model.classifier[i] for i in range(4)])
        vgg_model.to(device)
        vgg_model.eval()
        vgg_out = np.zeros([len(images), 4096])
        for i, data in tqdm(enumerate(data_loader)):
            with torch.no_grad():
                if verbose:
                    print(i)
                value = data
                test_value = Variable(value.to(device))
                test_value = test_value.float()
                out_ = vgg_model(test_value)
                out_ = out_.to('cpu')
                out_ = out_.detach().numpy()
                vgg_out[i * batch_size:i * batch_size + len(out_)] = out_

        if model_type == 'vgg':
            if verbose:
                print(vgg_out.shape)
            return vgg_out

    if model_type == 'resnet' or model_type == 'both':
        res_model = torch.load('symmodel')
        res_model.to(device)
        res_out = np.zeros([len(images), 512])
        for i, data in tqdm(enumerate(data_loader)):
            with torch.no_grad():
                if verbose:
                    print(i)
                value = data
                test_value = Variable(value.to(device))
                test_value = test_value.float()
                out_ = res_model(test_value)
                out_ = out_.to('cpu')
                out_ = out_.detach().numpy()
                res_out[i * batch_size:i * batch_size + len(out_)] = out_

        if model_type == 'resnet':
            if verbose:
                print(res_out.shape)
            return res_out

    if model_type == 'both':

        class Encoder(nn.Module):
            def __init__(self):
                super(Encoder, self).__init__()
                self.dense = nn.Linear(4096, 512)

            def forward(self, x):
                out = self.dense(x)
                return out

        class Decoder(nn.Module):
            def __init__(self):
                super(Decoder, self).__init__()
                self.dense = nn.Linear(512, 4096)

            def forward(self, x):
                out = self.dense(x)
                return out

        class Auto(nn.Module):
            def __init__(self, enc, dec):
                super().__init__()
                self.encoder = enc
                self.decoder = dec

            def forward(self, x):
                x = self.encoder(x)
                x = self.decoder(x)
                return x

        encoder = Encoder().to(device)
        decoder = Decoder().to(device)
        auto_model = Auto(encoder, decoder).to(device)
        optimizer = optim.Adam(auto_model.parameters(), lr=1e-4)
        train_iterator = torch.utils.data.DataLoader(vgg_out,
                                                     batch_size=batch_size,
                                                     shuffle=False)

        def loss_function(model, train_iterator, optimizer):

            model.train()
            train_loss = 0

            for x in tqdm(train_iterator, leave=True,
                          total=len(train_iterator)):
                x = x.to(device, dtype=torch.float)

                optimizer.zero_grad()

                predicted_x = model(x)

                # reconstruction loss
                loss = F.mse_loss(x, predicted_x, reduction='mean')

                # backward pass
                train_loss += loss.item()
                loss.backward()

                # update the weights
                optimizer.step()

            return train_loss

        for epoch in range(N_EPOCHS):
            train_loss = loss_function(auto_model, train_iterator, optimizer)
            train_loss /= len(train_iterator)
            print(f'Epoch {epoch}, Train Loss: {train_loss:.4f}')
            print('.............................')

        auto_out = np.zeros([len(vgg_out), 512])
        for i, x in tqdm(enumerate(train_iterator)):
            with torch.no_grad():
                value = x
                test_value = Variable(value.to(device))
                test_value = test_value.float()
                embedding = encoder(test_value)
                embedding1 = embedding.to('cpu')
                embedding1 = embedding1.detach().numpy()
                auto_out[i * batch_size:i * batch_size +
                         len(embedding1)] = embedding1

        combine_out = np.concatenate((auto_out, res_out), axis=1)

        if verbose:
            print(combine_out.shape)
        return combine_out

    else:

        raise NameError(
            'Please insert valid model, like "vgg","resnet" or "both".')
