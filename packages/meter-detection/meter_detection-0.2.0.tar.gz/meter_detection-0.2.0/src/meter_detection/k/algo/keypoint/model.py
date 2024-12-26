"""keras detection model"""

# using key point detectoin

import keras
from keras import layers

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 5
NUM_KEYPOINTS = 24 * 2  # 24 pairs each having x and y coordinates


def get_model():
  # Load the pre-trained weights of MobileNetV2 and freeze the weights
  backbone = keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
  )
  backbone.trainable = False

  inputs = layers.Input((IMG_SIZE, IMG_SIZE, 3))
  x = keras.applications.mobilenet_v2.preprocess_input(inputs)
  x = backbone(x)
  x = layers.Dropout(0.3)(x)
  x = layers.SeparableConv2D(
    NUM_KEYPOINTS, kernel_size=5, strides=1, activation="relu"
  )(x)
  outputs = layers.SeparableConv2D(
    NUM_KEYPOINTS, kernel_size=3, strides=1, activation="sigmoid"
  )(x)

  return keras.Model(inputs, outputs, name="keypoint_detector")
