from meter_detection.k.model import build_model
from meter_detection.k.schema import ModelParams


def get_model():
  return build_model(
    ModelParams(
      IMG_SIZE=224,
      NUM_KEYPOINTS=4,
    )
  )()
