import tensorflow as tf # pip install tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam
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
DATADIR = currentDirectory + "/dog_images"
CATEGORIES = list()
PATH_NAMES = list()
DOG_COUNTER = dict()
IMG_SIZE = 90

def get_categories( categories, datadir ):
    directory = os.fsencode(datadir)
    PATH_NAMES = list()
    for folder in os.listdir(directory):
        foldername = os.fsdecode(folder)
        d_index = foldername.find("-")
        dog_breed = foldername[d_index + 1:].lower().replace("_", " ")
        categories.append(dog_breed)
        PATH_NAMES.append(foldername)
        DOG_COUNTER[dog_breed] = 0

get_categories( CATEGORIES, DATADIR )
NUMCLASSES = len(CATEGORIES)
print( "CATEGORIES:", CATEGORIES )
print( "NUMCLASSES:", NUMCLASSES )

train_images = pickle.load( open("train_images.pickle","rb") ) # Get the formatted images from file
train_labels = pickle.load( open("train_labels.pickle", "rb" ) ) # Get the corresponding classifications from file

train_images = train_images/255.0 # Normalize the training images

### CREATING THE MODEL #########################################################
model = Sequential()
model.add( Conv2D(64, (3,3), input_shape = train_images.shape[1:]) )
model.add( Activation("relu"))
model.add( MaxPooling2D(pool_size=(2,2)) )

model.add( Conv2D(64, (3,3) ) )
model.add( Activation("relu"))
model.add( MaxPooling2D(pool_size=(2,2)) )

model.add( Flatten() )
model.add( Dense(64) )
model.add( Activation("relu"))
# Output layer
model.add( Dense(NUMCLASSES) ) # <-- Change this to the # of dog breeds we are testing
model.add( Activation('softmax') )

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
### TRAINING THE MODEL #########################################################
model.fit(train_images, train_labels, epochs=5)
# batch size = how many images to train each time through
# epochs = how many trainings to run
# validation_split = ???

model.save( 'trained.model' ) # Save the trained model to an outside file
test_loss, test_acc = model.evaluate( train_images, train_labels )
print('Test accuracy:', test_acc)
