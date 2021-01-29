import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import os

def which_one(img):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('terrafit/converted_keras/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    

    # Replace this with the path to your image
    image = Image.open(img)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    # print(prediction)

    a = ''
    for i in range(prediction.shape[1]):
        if abs(1-prediction.item(i)) < 0.2:
            a = str(i)

    # print(a)

    f = open('terrafit/converted_keras/labels.txt', 'r')
    l = f.read().splitlines()
    b = ''
    for el in l:
        if a in el:
            b = el[2:]

    d = []
    c = {}
    c['type'] = b
    d.append(c)
    return d

def cate():
    f = open('terrafit/converted_keras/labels.txt', 'r')
    l = f.read().splitlines()
    categories = []
    for el in l:
        categories.append(el[2:])

    return categories

def main(img):
    c = cate()
    w = which_one(img)[0]['type']
    if w == 'shirt':
        c.pop(0)
    elif w == 'shorts':
        c.pop(1)
        c.pop(1)
    else:
        c.pop(1)
        c.pop(1)
    return c

# print(which_one())
# print(cate())
# print(main())
