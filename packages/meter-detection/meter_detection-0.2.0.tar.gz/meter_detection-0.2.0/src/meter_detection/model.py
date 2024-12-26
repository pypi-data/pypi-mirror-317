"""A simple model for detection area"""

import torch
import torch.nn as nn


class DetectionAreaModel(nn.Module):
  def __init__(self):
    super().__init__()
    # self.model = torch.hub.load("facebookresearch/detr", "detr_resnet50_dc5")
    # self.model.load_state_dict(torch.load("detr_resnet50_dc5.pth"))

  def forward(self, x):
    return self.model(x)
