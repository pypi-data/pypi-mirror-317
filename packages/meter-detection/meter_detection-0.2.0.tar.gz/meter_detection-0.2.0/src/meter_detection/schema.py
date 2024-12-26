from pydantic import BaseModel


class Point(BaseModel):
  x: float
  y: float


class DetectionArea(BaseModel):
  top: Point
  bottom: Point
  # left: Point
  # right: Point
