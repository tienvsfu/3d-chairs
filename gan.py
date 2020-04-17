import sys
import os

import scipy.ndimage as nd
import scipy.io as io
import numpy as np
import matplotlib.pyplot as plt
import skimage.measure as sk
import trimesh
import pdb
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Activation, Conv3D, Conv3DTranspose, LeakyReLU, BatchNormalization

from tqdm import tqdm
from mpl_toolkits import mplot3d

# hyperparams as in
# http://3dgan.csail.mit.edu/papers/3dgan_nips.pdf
z_size = 100
strides = (2, 2, 2)
kernel_size = (4, 4, 4)
leak_value = 0.2
cube_len = 64

n_epochs   = 10000
batch_size = 100
g_lr       = 0.0025
d_lr       = 0.00001
beta       = 0.5

train_samples_dir = './samples/'
model_dir = './models/'

if not os.path.exists(train_samples_dir):
    os.makedirs(train_samples_dir)
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

def to_voxel(path):
    voxels = io.loadmat(path)['instance']
    voxels = np.pad(voxels,(1,1), 'constant', constant_values=(0,0))
    voxels = nd.zoom(voxels, (2,2,2), mode='constant', order=0)

    return voxels

def load_chairs():
    path = './drive/My Drive/train/'
    fl = [f for f in os.listdir(path) if f.endswith('.mat')][:2000]

    volumes = []

    for f in tqdm(fl):
        volumes.append(to_voxel(path + f))

    volumes = np.asarray(volumes, dtype=np.bool)
    return volumes

all_chairs = load_chairs()

def Generator():
    inputs = Input(shape=(1, 1, 1, z_size))

    x = Conv3DTranspose(filters=512, kernel_size=kernel_size, strides=(1, 1, 1), padding='valid')(inputs)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='relu')(x)

    x = Conv3DTranspose(filters=256, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='relu')(x)

    x = Conv3DTranspose(filters=128, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='relu')(x)

    x = Conv3DTranspose(filters=64, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='relu')(x)

    x = Conv3DTranspose(filters=1, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='sigmoid')(x) 

    model = Model(inputs=inputs, outputs=x)
    model.compile(loss='binary_crossentropy', optimizer="SGD")
    model.summary()

    return model

def Discriminator():
    inputs = Input(shape=(cube_len, cube_len, cube_len, 1))

    x = Conv3D(filters=64, kernel_size=kernel_size, strides=strides, padding='same')(inputs)
    x = BatchNormalization()(x, training=True)
    x = LeakyReLU(leak_value)(x)

    x = Conv3D(filters=128, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = LeakyReLU(leak_value)(x)

    x = Conv3D(filters=256, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = LeakyReLU(leak_value)(x)

    x = Conv3D(filters=512, kernel_size=kernel_size, strides=strides, padding='same')(x)
    x = BatchNormalization()(x, training=True)
    x = LeakyReLU(leak_value)(x)

    x = Conv3D(filters=1, kernel_size=kernel_size, strides=(1, 1, 1), padding='valid')(x)
    x = BatchNormalization()(x, training=True)
    x = Activation(activation='sigmoid')(x) 

    model = Model(inputs=inputs, outputs=x)
    optim = Adam(lr=d_lr, beta_1=0.9)
    # model.trainable = True
    model.compile(loss='binary_crossentropy', optimizer=optim)
    model.summary() 

    return model

def Adversary(g, d):
    optimizer = RMSprop(lr=0.0001, decay=3e-8)
    model = Sequential()
    model.add(g)
    model.add(d)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

generator = Generator()
discriminator = Discriminator()
adversary = Adversary(generator, discriminator)

a_losses = []
d_losses = []

def train(all_chairs):     
    z_sample = np.random.normal(0, 1, size=[batch_size, 1, 1, 1, z_size]).astype(np.float32)
    volumes = all_chairs[...,np.newaxis].astype(np.float)

    for epoch in range(n_epochs):
        idx = np.random.randint(len(volumes), size=batch_size)
        x = volumes[idx]
        z = np.random.normal(0, 1, size=[batch_size, 1, 1, 1, z_size]).astype(np.float32)

        generated_volumes = generator.predict(z, verbose=0)

        X = np.concatenate((x, generated_volumes))
        Y = np.reshape([1]*batch_size + [0]*batch_size, (-1,1,1,1,1))

        d_loss = discriminator.train_on_batch(X, Y)

        z = np.random.normal(0, 1, size=[batch_size, 1, 1, 1, z_size]).astype(np.float32)            
        a_loss = adversary.train_on_batch(z, np.reshape([1]*batch_size, (-1,1,1,1,1)))

        a_losses.append(a_loss[0])
        d_losses.append(d_loss)

        print(f"Epoch {epoch}, a_loss, {a_loss[0]}, d_loss: {d_loss}")

        if epoch % 5 == 0:
            generator.save_weights(f'{model_dir}generator_{epoch}.h5')
            discriminator.save_weights(f'{model_dir}discriminator_{epoch}.h5')

        generated_volumes = generator.predict(z_sample, verbose=0)
        generated_volumes = generated_volumes.squeeze(4)
        generated_volumes.dump(f'{train_samples_dir}/{epoch}.mat')