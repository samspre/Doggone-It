## Checkpoint 1: Verify Your Tensorflow
Most of these can be installed using the python pip utility, with the possible exception of python-tk.
Native install to your local version of python3.
You will need access to the follwoing python packages: 
- tensorflow
- keras
- matplotlib
- numpy
- pillow. 
Install them (you can probably use pip or conda depending on your python install). 
Once you are done, start python and run:
```
from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from PIL import ImageOps

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)
plt.plot((-2,4),(-6,6))
plt.show()

```
This should print out a version of TensorFlow in the console window and pop up a window:
###### INSERT IMAGE HERE

## Checkpoint 2: Run the TensorFlow Fashion Classification Example
Go to https://www.tensorflow.org/tutorials/keras/basic_classification to read more about the code.
Each image you want to test in should be:
- Greyscale
- 28x28 pixels
- Inverted (white is 0)
- Scaled between 0 and 1 instead of 0 and 255
