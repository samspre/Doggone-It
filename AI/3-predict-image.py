import cv2
import tensorflow as tf
import numpy as np

CATEGORIES = [ "pug", "husky", "retriever" ]

def prepare(filepath):
    IMG_SIZE = 90
    img_array = cv2.imread(filepath)
    new_array = cv2.resize( img_array, (IMG_SIZE,IMG_SIZE) )
    return new_array.reshape( -1, IMG_SIZE, IMG_SIZE, 3 )

model = tf.keras.models.load_model("trained.model") # Load the trained model from an outside file

'''
Below are examples of testing a single image on our trained model.
TO DO:
Take the image imputted by the user in our GUI.
Predict that image using this model.
Return the prediction result to the user in our GUI.
'''
prediction = model.predict([prepare('pug_test.png')])
print( "Percentages:", prediction[0] )
print( CATEGORIES[np.argmax(prediction)] )

prediction = model.predict([prepare('husky_test.png')])
print( "Percentages:", prediction[0] )
print( CATEGORIES[np.argmax(prediction)] )

prediction = model.predict([prepare('pug_test2.png')])
print( "Percentages:", prediction[0] )
print( CATEGORIES[np.argmax(prediction)] )

prediction = model.predict([prepare('retriever_test.png')])
print( "Percentages:", prediction[0] )
print( CATEGORIES[np.argmax(prediction)] )
