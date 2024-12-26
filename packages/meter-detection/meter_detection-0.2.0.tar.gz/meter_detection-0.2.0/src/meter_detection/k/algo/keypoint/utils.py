import json
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image

PROJECT_ROOT = "/home/xiuhao/work/meter-project/cnn-lstm-ctc/src/detection-area"
IMG_DIR = f"{PROJECT_ROOT}/examples/standford/Images"
KEYPOINT_DEF = f"{PROJECT_ROOT}/examples/standford/keypoint_definitions.csv"
JSON = f"{PROJECT_ROOT}/examples/standford/StanfordExtra_V12/StanfordExtra_v12.json"


def get_keypoint_def():
  return pd.read_csv(KEYPOINT_DEF)


def get_json_dict():
  # Load the ground-truth annotations.
  with open(JSON) as infile:
    json_data = json.load(infile)

  # Set up a dictionary, mapping all the ground-truth information
  # with respect to the path of the image.
  json_dict = {i["img_path"]: i for i in json_data}
  return json_dict


def gen_get_dog(IMG_DIR, json_dict):
  # Utility for reading an image and for getting its annotations.
  def get_dog(name):
    data = json_dict[name]
    img_data = plt.imread(os.path.join(IMG_DIR, data["img_path"]))
    # If the image is RGBA convert it to RGB.
    if img_data.shape[-1] == 4:
      img_data = img_data.astype(np.uint8)
      img_data = Image.fromarray(img_data)
      img_data = np.array(img_data.convert("RGB"))
    data["img_data"] = img_data

    return data

  return get_dog


# Load the metdata definition file and preview it.
keypoint_def = get_keypoint_def()

# Set up a dictionary, mapping all the ground-truth information
# with respect to the path of the image.
json_dict = get_json_dict()
get_dog = gen_get_dog(IMG_DIR, json_dict)
