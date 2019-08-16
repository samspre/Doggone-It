import numpy as np # pip install numpy
import matplotlib.pyplot as plt # pip install matplotlib
import os
import cv2 # pip install openvc-python


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

def create_training_data():

    for i in range(len(CATEGORIES)): # iterate through each breed we have pictures for
        path = os.path.join( DATADIR, PATH_NAMES[i] ) # gets into the path to the breed's pictures
        class_num = i # Need to map each breed name to a number
        for img in os.listdir(path): # iterate through all of the images
            try:
                img_array = cv2.imread(os.path.join(path,img) ) # convert image immediately to an array
                '''
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GREYSCALE ) to convert it to greyscale
                If color is not that essential, use this line instead^^^
                '''

                #How to display current image:
                # plt.imshow(img_array)
                # plt.show()

                new_array = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE) ) # Need every picture to be a normalized size
                '''
                How to display current image:
                plt.imshow(new_array)
                plt.show()
                '''
                training_data.append([new_array, class_num]) # Append the image and its classification to the training_data
            except Exception as e: # Some images could be broken, just skip over these
                pass


# currentDirectory = os.getcwd()
# DATADIR = currentDirectory + "/dog_images"
# CATEGORIES = list()
# PATH_NAMES = list()
# DOG_COUNTER = dict()
# IMG_SIZE = 90 # Higher -> better quality image
# get_categories( CATEGORIES, DATADIR )
# print(CATEGORIES)
# training_data =[]
# create_training_data()
# print( "Training data length:", len(training_data) )

#for features, label in training_data:
#    DOG_COUNTER[CATEGORIES[label]] += 1

#print(DOG_COUNTER)
'''
It's really important that the training data is balanced.
This is an issue that can be fixed by scraping more images from online.
'''

# import random
# random.shuffle( training_data ) # Shuffle the data, so not everything is all one thing. and then everything is all another thing.

# train_images =[] # An array to hold just the images
# train_labels = [] # An array to hold the corresponding classifications for those images
# for features, label in training_data: # fill the arrays
#     train_images.append( features )
#     train_labels.append( label )

# train_images = np.array(train_images).reshape( -1,IMG_SIZE,IMG_SIZE, 3 ) # each image must be a numpy array and must be reshaped
#                                                                    #^^^^ 1 = Greyscale; 3 = RGB
# import pickle
# pickle_out = open( "train_images.pickle","wb" ) # Write the formatted images to a file
# pickle.dump( train_images, pickle_out )
# pickle_out.close()

# pickle_out = open( "train_labels.pickle","wb" ) # Write the corresponding classifications to a file
# pickle.dump( train_labels, pickle_out )
# pickle_out.close()
