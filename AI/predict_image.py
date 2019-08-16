import cv2
import os
import tensorflow as tf
import sys
def prepare(filepath):
    IMG_SIZE = 90
    img_array = cv2.imread(filepath)
    new_array = cv2.resize( img_array, (IMG_SIZE,IMG_SIZE) )
    return new_array.reshape( -1, IMG_SIZE, IMG_SIZE, 3 )

def get_categories( categories, datadir ):
    directory = os.fsencode(datadir)
    for folder in os.listdir(directory):
        foldername = os.fsdecode(folder)
        d_index = foldername.find("-")
        dog_breed = foldername[d_index + 1:].lower().replace("_", " ")
        categories.append(dog_breed)

def predict_image(image_path):
    model = tf.keras.models.load_model("trained.model") # Load the trained model from an outside file
    prediction = model.predict(prepare(image_path), verbose=1)
    results = dict()
    currentDirectory = os.getcwd()
    CATEGORIES = list()
    DATADIR = currentDirectory + "\\AI\\dog_images"
    get_categories(CATEGORIES, DATADIR)
    for i in range(len(CATEGORIES)):
        results[CATEGORIES[i]] = 100 * int(prediction[0][i])
    top_three = sorted(results.items(), reverse=True, key=lambda kv: kv[1])
    print(top_three, file=sys.stderr)    
    return top_three
'''
Below are examples of testing a single image on our trained model.
TO DO:
Take the image imputted by the user in our GUI.
Predict that image using this model.
Return the prediction result to the user in our GUI.
'''
# prediction = model.predict([prepare('pug_test.png')])
# print( CATEGORIES[int(prediction[0][0])] )

# prediction = model.predict([prepare('husky_test.png')])
# print( CATEGORIES[int(prediction[0][0])] )

# prediction = model.predict([prepare('pug_test2.png')])
# print( CATEGORIES[int(prediction[0][0])] )

# results = predict_image("pug_test.png")
# print(results)