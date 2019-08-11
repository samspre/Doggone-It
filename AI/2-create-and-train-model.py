import tensorflow as tf # pip install tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.metrics import categorical_accuracy
import pickle
import time
from PIL import Image # pip install pillow
import PIL.ImageOps
import numpy as np # pip install numpy
import matplotlib.pyplot as plt # pip install matplotlib
import os
import cv2 # pip install openvc-python

currentDirectory = os.getcwd()
TESTDIR = currentDirectory
CATEGORIES = [ "pug", "husky" ]
IMG_SIZE = 90

train_images = pickle.load( open("train_images.pickle","rb") ) # Get the formatted images from file
train_labels = pickle.load( open("train_labels.pickle", "rb" ) ) # Get the corresponding classifications from file

train_images = train_images/255.0 # Normalize the training images

'''
Below is where we create our model.
The commented out model is an example of a binary model.
The uncommented model is an example of a categorical model.
Both can be edited to increase accuracy and reliability.
'''
# model = Sequential()
# model.add( Conv2D(64, (3,3), input_shape = train_images.shape[1:]) )
# model.add( Activation("relu"))
# model.add( MaxPooling2D(pool_size=(2,2)) )
#
# model.add( Conv2D(64, (3,3) ) )
# model.add( Activation("relu"))
# model.add( MaxPooling2D(pool_size=(2,2)) )
#
# model.add( Flatten() )
# model.add( Dense(64) )
#
# # Output layer
# model.add( Dense(1) )
# model.add( Activation('sigmoid') )
#
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

model = keras.Sequential([
    keras.layers.Flatten(input_shape = train_images.shape[1:]), # Transforms the format from a 2D array (28*28) to a 1D array of pixels (784)
    keras.layers.Dense(128, activation=tf.nn.relu), # 128 nodes, for neurons
    keras.layers.Dense(10, activation=tf.nn.softmax) # 10-node softmax layer, returns an array of 10 probability scores that sum to 1
])

# model.compile(optimizer='adam',
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(train_images, train_labels, epochs=5)


model.fit( train_images, train_labels, batch_size=32, epochs=100, validation_split=0.1 )
# batch size = how many images to train each time through
# epochs = how many trainings to run
# validation_split = ???
model.save( 'trained.model') # Save the trained model to an outside file

test_loss, test_acc = model.evaluate( train_images, train_labels )
print('Test accuracy:', test_acc)
