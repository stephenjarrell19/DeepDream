from scipy.ndimage import zoom
import numpy as np
import tensorflow as tf
import cv2
import IPython.display as display
import PIL.Image
import os
import imutils

def clipped_zoom(img, zoom_factor, rotate = False):

    if rotate:
        img = imutils.rotate(img.numpy(), angle = 0.5)
    h, w = img.shape[:2]

    # For multichannel images we don't want to apply the zoom factor to the RGB
    # dimension, so instead we create a tuple of zoom factors, one per array
    # dimension, with 1's for any trailing dimensions after the width and height.
    zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    # Zooming out
    if zoom_factor < 1:

        # Bounding box of the zoomed-out image within the output array
        zh = int(np.round(h * zoom_factor))
        zw = int(np.round(w * zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

        # Zero-padding
        out = np.zeros_like(img)
        out[top:top+zh, left:left+zw] = zoom(img, zoom_tuple)

    # Zooming in
    elif zoom_factor > 1:

        # Bounding box of the zoomed-in region within the input array
        zh = int(np.round(h / zoom_factor))
        zw = int(np.round(w / zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

        out = zoom(img[top:top+zh, left:left+zw], zoom_tuple)

        # `out` might still be slightly larger than `img` due to rounding, so
        # trim off any extra pixels at the edges
        trim_top = ((out.shape[0] - h) // 2)
        trim_left = ((out.shape[1] - w) // 2)
        out = out[trim_top:trim_top+h, trim_left:trim_left+w]

    # If zoom_factor == 1, just return the input array
    else:
        out = img
    return out

# Randomly shift the image to avoid tiled boundaries.
def random_roll(img, maxroll):
  
    shift = tf.random.uniform(shape=[2], minval=-maxroll, maxval=maxroll, dtype=tf.int32)
    img_rolled = tf.roll(img, shift=shift, axis=[0,1])
    return shift, img_rolled


# Normalize an image
def deprocess(img):
   
    img = 255*(img + 1.0)/2.0
    return tf.cast(img, tf.uint8)

# Display an image
def show(img):
   
    display.display(PIL.Image.fromarray(np.array(img)))
    
def save_image(img, directory = 'outputs', file_name = 'test'):
    if type(img) != np.ndarray:
        img = img.numpy()
    #img = img * 255
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        pass
    #img = tf.image.resize(img, ((500,500)))
    #img = tf.image.convert_image_dtype(img/255.0, dtype=tf.uint8)
    
    if os.path.isdir(directory) == False:
        os.mkdir(directory)
        
    cv2.imwrite(directory + '/' + file_name + '.jpg', img)
