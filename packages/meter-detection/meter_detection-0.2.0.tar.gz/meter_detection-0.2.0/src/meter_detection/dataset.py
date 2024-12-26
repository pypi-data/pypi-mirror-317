import json
import pathlib
import typing as t

import matplotlib.pyplot as plt
import numpy as np
import torch
from meterviewer.generator.schema import MeterDB
from PIL import ImageFile
from torch.utils.data import Dataset

# 设置允许加载截断的图像
ImageFile.LOAD_TRUNCATED_IMAGES = True


class MeterDBLoader(object):
  """MeterDB format data loader"""

  data: MeterDB

  def read_data(self, file_path: pathlib.Path) -> MeterDB:
    """read data from file_path"""
    with open(file_path, "r") as f:
      data = json.load(f)
    self.data: MeterDB = MeterDB.model_validate(data)
    return self.data

  def get_img(self, dataset_dir: pathlib.Path, i: int) -> np.ndarray:
    assert isinstance(dataset_dir, pathlib.Path), "dataset_dir must be a pathlib.Path"
    return plt.imread(dataset_dir / self.data.data[i].filepath)

  def __len__(self):
    return len(self.data.data)

  def get_labels(self, i: int) -> list[tuple[float, float]]:
    point_1 = [self.data.data[i].xmin, self.data.data[i].ymin]
    point_2 = [self.data.data[i].xmax, self.data.data[i].ymin]
    point_3 = [self.data.data[i].xmax, self.data.data[i].ymax]
    point_4 = [self.data.data[i].xmin, self.data.data[i].ymax]
    return [
      point_1,
      point_2,
      point_3,
      point_4,
    ]

  def get_samples(self, data_dir: pathlib.Path, start: int, end: int):
    return {
      "img_data": [self.get_img(data_dir, i) for i in range(start, end)],
      "joints": [self.get_labels(i) for i in range(start, end)],
    }


class DetectionAreaDataset(Dataset):
  def __init__(self, root_dir: pathlib.Path, stage: t.Literal["train", "test"]):
    """detect area dataset"""
    self.root_dir = root_dir
    self.loader = MeterDBLoader()
    self.load_dataset(stage=stage)

  def load_dataset(self, stage: t.Literal["train", "test"]):
    """load dataset from root_dir"""
    self.data = self.loader.read_data(self.root_dir / f"meterdb_{stage}.json")

  def __len__(self):
    return len(self.data)

  def __getitem__(self, index):
    return self.data[index]
