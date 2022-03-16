import torch.nn as nn
import torch

class PatchAntenna1ConvAutoEncoder(nn.Module):
    def __init__(self, Latent_size = 10):
        super(PatchAntenna1ConvAutoEncoder, self).__init__()


        self.conv_encoder1 = nn.Conv2d(in_channels=4,
                                    out_channels=8,
                                    kernel_size=3,
                                    padding = 2,
                                    stride=2)
        self.conv_encoder2 = nn.Conv2d(in_channels=8,
                                    out_channels=16,
                                    kernel_size=3,
                                    stride=2)


        self.linear_to_latent = nn.Linear(in_features=16*90,
                                        out_features= Latent_size)
        
        self.latent_to_linear = nn.Linear(in_features=Latent_size,
                                        out_features= 16*90)

        self.conv_decoder1 =  nn.ConvTranspose2d(in_channels=16,
                                        out_channels=8,
                                        kernel_size=3,
                                        stride=2,
                                        padding = (0,0),
                                        output_padding=(0,1))


        self.conv_decoder2 =  nn.ConvTranspose2d(in_channels=8,
                                        out_channels=4,
                                        kernel_size=3,
                                        padding=2,
                                        stride=2)

        self.activation = nn.LeakyReLU()


    def encode(self,x):
        x = x.reshape(-1,4,3,361) # [Batch_size, Channels, Height, Width]
        x = self.conv_encoder1(x)
        x = self.activation(x)
        x = self.conv_encoder2(x)
        x = self.activation(x)
        x = x.flatten()
        latent_space = self.linear_to_latent(x)

        return latent_space

    def decode(self,y):
        y = self.latent_to_linear(y)
        y = self.activation(y)
        y = y.reshape(1,16,1,90)
        y = self.conv_decoder1(y)
        y = self.activation(y)
        y = self.conv_decoder2(y).reshape(-1,361,3,4)
        return y


    def forward(self, x):

        self.latent_space = self.encode(x)
        output = self.decode(self.latent_space)

        return output


class PatchAntenna1ConvVAE(nn.Module):

    def __init__(self, Latent_size = 10):
        super(PatchAntenna1ConvVAE, self).__init__()


        self.conv_encoder1 = nn.Conv2d(in_channels=4,
                                    out_channels=8,
                                    kernel_size=3,
                                    padding = 2,
                                    stride=2)
        self.conv_encoder2 = nn.Conv2d(in_channels=8,
                                    out_channels=16,
                                    kernel_size=3,
                                    stride=2)


        self.linear_to_latent = nn.Linear(in_features=16*90,
                                        out_features= Latent_size)
        
        self.latent_to_linear = nn.Linear(in_features=Latent_size,
                                        out_features= 16*90)

        self.conv_decoder1 =  nn.ConvTranspose2d(in_channels=16,
                                        out_channels=8,
                                        kernel_size=3,
                                        stride=2,
                                        padding = (0,0),
                                        output_padding=(0,1))


        self.conv_decoder2 =  nn.ConvTranspose2d(in_channels=8,
                                        out_channels=4,
                                        kernel_size=3,
                                        padding=2,
                                        stride=2)

        self.activation = nn.LeakyReLU()


    def encode(self,x):
        x = x.reshape(-1,4,3,361) # [Batch_size, Channels, Height, Width]
        x = self.conv_encoder1(x)
        x = self.activation(x)
        x = self.conv_encoder2(x)
        x = self.activation(x)
        x = x.flatten()
        latent_space = self.linear_to_latent(x)

        return latent_space

    def decode(self,y):
        y = self.latent_to_linear(y)
        y = self.activation(y)
        y = y.reshape(1,16,1,90)
        y = self.conv_decoder1(y)
        y = self.activation(y)
        y = self.conv_decoder2(y).reshape(-1,361,3,4)
        return y

    def reparameterize(self, mu, log_var):
        """
        :param mu: mean from the encoder's latent space
        :param log_var: log variance from the encoder's latent space
        """
        std = torch.exp(0.5*log_var) # standard deviation
        eps = torch.randn_like(std) # `randn_like` as we need the same size
        sample = mu + (eps * std) # sampling as if coming from the input space
        return sample

    def forward(self, x):

        self.latent_space = self.encode(x)
        output = self.decode(self.latent_space)

        return output

