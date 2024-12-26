import pathlib
import typing as t

import keras
import numpy as np
from imgaug.augmentables.kps import Keypoint, KeypointsOnImage

from meter_detection.dataset import MeterDBLoader
from meter_detection.k.schema import ModelParams


def build_dataset(params: ModelParams) -> t.Type[keras.utils.PyDataset]:
  class KeyPointsDataset(keras.utils.PyDataset):
    def __init__(
      self,
      jsondb_path: pathlib.Path,
      aug,
      batch_size=params.BATCH_SIZE,
      train=True,
      **kwargs,
    ):
      super().__init__(**kwargs)
      self.aug = aug
      self.batch_size = batch_size
      self.loader = MeterDBLoader()
      self.loader.read_data(jsondb_path)
      self.train = train
      self.on_epoch_end()

    def __len__(self):
      return len(self.loader) // self.batch_size

    def on_epoch_end(self):
      self.indexes = np.arange(len(self.loader))
      if self.train:
        np.random.shuffle(self.indexes)

    def __getitem__(self, index):
      indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]
      (images, keypoints) = self.__data_generation(indexes)

      return (images, keypoints)

    def get_meter(self, i):
      return {
        "img_data": self.loader.get_img(pathlib.Path(params.root_dir), i),
        "joints": self.loader.get_labels(i),
      }

    def __data_generation(self, indexes):
      batch_images = np.empty(
        (self.batch_size, params.IMG_SIZE, params.IMG_SIZE, 3), dtype="int"
      )
      batch_keypoints = np.empty(
        (self.batch_size, 1, 1, params.NUM_KEYPOINTS * 2), dtype="float32"
      )

      for i, key in enumerate(indexes):
        data = self.get_meter(key)
        current_keypoint = np.array(data["joints"])[:, :2]
        kps = []

        # To apply our data augmentation pipeline, we first need to
        # form Keypoint objects with the original coordinates.
        for j in range(0, len(current_keypoint)):
          kps.append(Keypoint(x=current_keypoint[j][0], y=current_keypoint[j][1]))

        # We then project the original image and its keypoint coordinates.
        current_image = data["img_data"]
        kps_obj = KeypointsOnImage(kps, shape=current_image.shape)

        # Apply the augmentation pipeline.
        (new_image, new_kps_obj) = self.aug(image=current_image, keypoints=kps_obj)
        batch_images[i,] = new_image

        # Parse the coordinates from the new keypoint object.
        kp_temp = []
        for keypoint in new_kps_obj:
          kp_temp.append(np.nan_to_num(keypoint.x))
          kp_temp.append(np.nan_to_num(keypoint.y))

        # More on why this reshaping later.
        batch_keypoints[i,] = np.array(kp_temp).reshape(1, 1, params.NUM_KEYPOINTS * 2)

      # Scale the coordinates to [0, 1] range.
      batch_keypoints = batch_keypoints / params.IMG_SIZE

      return (batch_images, batch_keypoints)

  return KeyPointsDataset
