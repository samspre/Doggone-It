from __future__ import absolute_import, division, print_function, unicode_literals
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
from PIL import Image
import PIL.ImageOps
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# Import and load the data
fashion_mnist = keras.datasets.fashion_mnist

# The train_images and train_labels arrays are the training set—the data the model uses to learn.
# The model is tested against the test set, the test_images, and test_labels arrays.
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# The following shows there are 60,000 images in the training set, with each image represented as 28x28 pixels
print(train_images)
# Likewise, there are 60,000 labels in the training set
print( len(train_labels) )
# Each label is an integer between 0 and 9
print( train_labels )
# There are 10,000 images in the test set. Each represented as 28 x 28 pixels
print( test_images.shape )
# And the test set contains 10,000 images labels
print( len( test_labels ) )

# If you inspect the first image in the training set, you will see that the pixel values fall in the range 0 to 255
# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()
# We scale these values to a range of 0 to 1 before feeding to the neural network model
# FOr this, we divide the values by 255. It's important that the training set and the testing set are
# processed in the same way
train_images = train_images / 255.0
test_images = test_images / 255.0

# Display the first 25 images from the training set and display the class name below each image
# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[train_labels[i]])
# plt.show()

# BUILD THE MODEL
# Setup the layers
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), # Transforms the format from a 2D array (28*28) to a 1D array of pixels (784)
    keras.layers.Dense(128, activation=tf.nn.relu), # 128 nodes, for neurons
    keras.layers.Dense(10, activation=tf.nn.softmax) # 10-node softmax layer, returns an array of 10 probability scores that sum to 1
])

# Compile the model
# Loss function = measures how accurate the model is during training. Minimize this function to "steer" the model in the right direction
# Optimizer = This is how the model is updated based on the data it sees and its loss function
# Metrics = used to monitor the training and testing steps. THe following example uses accuracy, the fraction of the images that are correctly classified
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
# 1. Feed the training data to the model
# 2. The model learns to associate images and labels
# 3. We ask the model to make predictions about a test set.
model.fit(train_images, train_labels, epochs=5)

# Evaluate accuracy
# Compare how the model performs on the test dataset
test_loss, test_acc = model.evaluate(test_images, test_labels)
# The gap between training accuracy and test accuracy is an example of overfitting (when an ML model performs worse on new data than on their training data)
print('Test accuracy:', test_acc)

# Make predictions
predictions = model.predict(test_images)
# First prediction
print( predictions[0] )
# which label has the highest confidence value:
print( np.argmax(predictions[0]) )
# what the image actually is labeled
print( test_labels[0] )

# Graph this to look at the full set of 10 class predictions
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

# Look at the 0th image, predictions, and prediction array
# i = 0
# plt.figure(figsize=(6,3))
# plt.subplot(1,2,1)
# plot_image(i, predictions, test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions,  test_labels)
# plt.show()
#
# i = 12
# plt.figure(figsize=(6,3))
# plt.subplot(1,2,1)
# plot_image(i, predictions, test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions,  test_labels)
# plt.show()

# Correct prediction labels are blue and incorrect in red
# Plot the first X test images, their predicted label, and the true label
# Color correct predictions in blue, incorrect predictions in red
# num_rows = 5
# num_cols = 3
# num_images = num_rows*num_cols
# plt.figure(figsize=(2*2*num_cols, 2*num_rows))
# for i in range(num_images):
#   plt.subplot(num_rows, 2*num_cols, 2*i+1)
#   plot_image(i+9000, predictions, test_labels, test_images)
#   plt.subplot(num_rows, 2*num_cols, 2*i+2)
#   plot_value_array(i+9000, predictions, test_labels)
# plt.show()

# Finally, use the trained model to make a prediction about a single image
# Grab an image from the test dataset
img = test_images[0]
print(img.shape)
# tf.keras models are optimized to make predictions on a batch, so even though we're using a single image,
# we need to add it to a list
# Add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))
print(img.shape)
# Now predict the iamge
# model.predict returns a list of ints, on for each image in the batch of data
# Grab the predictions for our (only) image in the batch
predictions_single = model.predict(img)
print(predictions_single)
plot_value_array(0, predictions_single, test_labels)
plt.xticks(range(10), class_names, rotation=45)
# plt.show()
prediction_result = np.argmax(predictions_single[0])
print(prediction_result)

# CHECKPOINT 3
print( "\nCHECKPOINT 3" )
im1 = Image.open( "OriginalImage1.png" )
im1 = im1.convert( mode = 'L' )
im1 = im1.resize( (28,28) )
im1 = PIL.ImageOps.invert( im1 )
im1.show()

im2 = Image.open( "OriginalImage2.png" )
im2 = im2.convert( mode = 'L' )
im2 = im2.resize( (28,28) )
im2 = PIL.ImageOps.invert( im2 )
im2.show()

im3 = Image.open( "OriginalImage3.png" )
im3 = im3.convert( mode = 'L' )
im3 = im3.resize( (28,28) )
im3 = PIL.ImageOps.invert( im3 )
im3.show()

im1 = np.array(im1)
im2 = np.array(im2)
im3 = np.array(im3)

im1 = ( np.expand_dims(im1,0) )
# Make predictions
predictions_single = model.predict( im1 )
# First prediction
print( "Image 1:", predictions_single, end=' ' )
# which label has the highest confidence value:
print(  np.argmax(predictions_single), class_names[np.argmax(predictions_single)] )

im2 = ( np.expand_dims(im2,0) )
# Make predictions
predictions_single = model.predict( im2 )
# First prediction
print( "Image 2:", predictions_single, end=' ' )
# which label has the highest confidence value:
print( np.argmax(predictions_single), class_names[np.argmax(predictions_single)] )

im3 = ( np.expand_dims(im3,0) )
# Make predictions
predictions_single = model.predict( im3 )
# First prediction
print( "Image 3:", predictions_single, end=' ' )
# which label has the highest confidence value:
print( np.argmax(predictions_single), class_names[np.argmax(predictions_single)] )
