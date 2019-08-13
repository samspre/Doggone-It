import cv2
import tensorflow as tf

CATEGORIES = [ "pug", "husky" ]

def prepare(filepath):
    IMG_SIZE = 90
    img_array = cv2.imread(filepath)
    new_array = cv2.resize( img_array, (IMG_SIZE,IMG_SIZE) )
    return new_array.reshape( -1, IMG_SIZE, IMG_SIZE, 3 )


def predict_image(image_path):
    model = tf.keras.models.load_model("trained.model") # Load the trained model from an outside file
    prediction = model.predict(prepare(image_path), verbose=1)
    results = dict()
    for i in range(len(CATEGORIES)):
        results[CATEGORIES[i]] = 100 * int(prediction[0][i])
    return results
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