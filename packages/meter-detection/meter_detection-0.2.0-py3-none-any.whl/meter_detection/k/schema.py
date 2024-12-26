from pydantic import BaseModel


class ModelParams(BaseModel):
  IMG_SIZE: int = 224
  BATCH_SIZE: int = 64
  EPOCHS: int = 5
  NUM_KEYPOINTS: int = 24 * 2  # 24 pairs each having x and y coordinates
  root_dir: str  # root dir for dataset
