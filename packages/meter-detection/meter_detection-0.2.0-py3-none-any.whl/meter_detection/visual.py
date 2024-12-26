import numpy as np
import pandas as pd
from imgaug.augmentables.kps import KeypointsOnImage
from matplotlib import pyplot as plt

# from imgaug.augmentables.kps import Keypoint
PROJECT_ROOT = "/home/xiuhao/work/meter-project/cnn-lstm-ctc/src/detection-area"
KEYPOINT_DEF = f"{PROJECT_ROOT}/examples/standford/keypoint_definitions.csv"


def get_keypoint_def():
  return pd.read_csv(KEYPOINT_DEF)


# Extract the colours and labels.
keypoint_def = get_keypoint_def()
colours = keypoint_def["Hex colour"].values.tolist()
colours = ["#" + colour for colour in colours]


def visualize_keypoints(images, keypoints):
  fig, axes = plt.subplots(nrows=len(images), ncols=2, figsize=(16, 12))
  [ax.axis("off") for ax in np.ravel(axes)]

  for (ax_orig, ax_all), image, current_keypoint in zip(axes, images, keypoints):
    ax_orig.imshow(image)
    ax_all.imshow(image)

    # If the keypoints were formed by `imgaug` then the coordinates need
    # to be iterated differently.
    if isinstance(current_keypoint, KeypointsOnImage):
      for idx, kp in enumerate(current_keypoint.keypoints):
        ax_all.scatter(
          [kp.x],
          [kp.y],
          c=colours[idx],
          marker="x",
          s=50,
          linewidths=5,
        )
    else:
      current_keypoint = np.array(current_keypoint)
      # Since the last entry is the visibility flag, we discard it.
      current_keypoint = current_keypoint[:, :2]
      for idx, (x, y) in enumerate(current_keypoint):
        ax_all.scatter([x], [y], c=colours[idx], marker="x", s=50, linewidths=5)

  plt.tight_layout(pad=2.0)
  plt.show()
