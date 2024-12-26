import keras
from keras import layers

from .schema import ModelParams


def build_model(params: ModelParams):
  def get_model():
    # Load the pre-trained weights of MobileNetV2 and freeze the weights
    backbone = keras.applications.MobileNetV2(
      weights="imagenet",
      include_top=False,
      input_shape=(params.IMG_SIZE, params.IMG_SIZE, 3),
    )
    backbone.trainable = False

    inputs = layers.Input((params.IMG_SIZE, params.IMG_SIZE, 3))
    x = keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = backbone(x)
    x = layers.Dropout(0.3)(x)
    x = layers.SeparableConv2D(
      params.NUM_KEYPOINTS * 2, kernel_size=5, strides=1, activation="relu"
    )(x)
    outputs = layers.SeparableConv2D(
      params.NUM_KEYPOINTS * 2, kernel_size=3, strides=1, activation="sigmoid"
    )(x)

    return keras.Model(inputs, outputs, name="keypoint_detector")

  return get_model
