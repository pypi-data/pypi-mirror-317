import imgaug.augmenters as iaa

from meter_detection.k.schema import ModelParams


def get_train_aug(params: ModelParams):
  train_aug = iaa.Sequential(
    [
      iaa.Resize(params.IMG_SIZE, interpolation="linear"),
      iaa.Fliplr(0.3),
      # `Sometimes()` applies a function randomly to the inputs with
      # a given probability (0.3, in this case).
      iaa.Sometimes(0.3, iaa.Affine(rotate=10, scale=(0.5, 0.7))),
    ]
  )
  return train_aug


def get_test_aug(params: ModelParams):
  test_aug = iaa.Sequential([iaa.Resize(params.IMG_SIZE, interpolation="linear")])
  return test_aug
