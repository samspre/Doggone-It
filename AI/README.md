## Step 1:
#### Run ```1-create-training-data.py``` to pull sample dog photos and format them into a way the AI can understand.     
Included in this directory is a folder ```dog_photos```. Feel free to upload any sample photos you want to train the AI with to this folder. GitHub only allows 100 files to be uploaded at a time. You'll want more photos to increase the accuracy and reliability of the AI model.
## Step 2:
#### Run ```2-create-and-train-model.py``` to create and train the AI model.
The creation of the model can be changed to increase accuracy and reliability. Feel free to mess around with it.
## Step 3:
#### Run ```3-predict-image.py``` to test the AI model on ANY image.
Included in this directory are three test photos. Use these as an example when testing your own images.     
The goal is to connect this file to our UI, so that
- the user can input an image with our UI
- this program can use the model to predict that image
- the program will return to the UI the prediction result
