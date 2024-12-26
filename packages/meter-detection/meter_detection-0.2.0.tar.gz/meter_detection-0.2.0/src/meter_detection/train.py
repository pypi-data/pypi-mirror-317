# using lit to train model

import lightning as L
import torch
import torch.nn as nn

from .dataset import DetectionAreaDataset
from .model import DetectionAreaModel


class DetectionAreaTrainer(L.LightningModule):
  def __init__(self, model: DetectionAreaModel):
    super().__init__()
    self.model = model

  def forward(self, x):
    return self.model(x)

  def training_step(self, batch, batch_idx):
    x, y = batch
    y_hat = self.forward(x)
    loss = nn.functional.mse_loss(y_hat, y)
    return loss

  def configure_optimizers(self):
    return torch.optim.Adam(self.model.parameters(), lr=1e-3)


def main():
  model = DetectionAreaModel()
  trainer = DetectionAreaTrainer(model)
  dataset = DetectionAreaDataset(root_dir="data")
  trainer.fit(dataset)


if __name__ == "__main__":
  main()
