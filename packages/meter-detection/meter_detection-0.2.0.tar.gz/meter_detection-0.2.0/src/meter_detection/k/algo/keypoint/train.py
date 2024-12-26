import imgaug.augmenters as iaa
import keras
import numpy as np

from meter_detection.data_process import get_test_aug, get_train_aug
from meter_detection.visual import visualize_keypoints

from .dataset import KeyPointsDataset
from .model import EPOCHS, IMG_SIZE, get_model
from .utils import get_dog, json_dict

# Select four samples randomly for visualization.
samples = list(json_dict.keys())
num_samples = 4
selected_samples = np.random.choice(samples, num_samples, replace=False)

images, keypoints = [], []

for sample in selected_samples:
  data = get_dog(sample)
  image = data["img_data"]
  keypoint = data["joints"]

  images.append(image)
  keypoints.append(keypoint)

np.random.shuffle(samples)
train_keys, validation_keys = (
  samples[int(len(samples) * 0.15) :],
  samples[: int(len(samples) * 0.15)],
)


def train():
  train_aug, test_aug = get_train_aug(), get_test_aug()

  train_dataset = KeyPointsDataset(
    train_keys, train_aug, workers=2, use_multiprocessing=True
  )
  validation_dataset = KeyPointsDataset(
    validation_keys, test_aug, train=False, workers=2, use_multiprocessing=True
  )

  print(f"Total batches in training set: {len(train_dataset)}")
  print(f"Total batches in validation set: {len(validation_dataset)}")

  sample_images, sample_keypoints = next(iter(train_dataset))
  assert sample_keypoints.max() == 1.0
  assert sample_keypoints.min() == 0.0

  sample_keypoints = sample_keypoints[:4].reshape(-1, 24, 2) * IMG_SIZE
  visualize_keypoints(sample_images[:4], sample_keypoints)
  model = get_model()
  model.compile(loss="mse", optimizer=keras.optimizers.Adam(1e-4))
  model.fit(train_dataset, validation_data=validation_dataset, epochs=EPOCHS)


def show():
  visualize_keypoints(images, keypoints)
