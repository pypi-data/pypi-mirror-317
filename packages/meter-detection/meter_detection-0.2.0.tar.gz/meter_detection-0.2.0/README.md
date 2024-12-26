# Detection model for Reading Area Detection

Detection models for meter reading area.

We use stanford-extra dataset as the basic dataset.

## Install

`pip install meter_detection`

Install keras and torch by yourself.

## Features

- [x] To train with stanford-extra dataset, using `examples/notebooks/keypoint_detection.ipynb`.
- [x] train with meter dataset, just run `examples/notebooks/meter_detection.ipynb`.
- [x] I want to use keras as the deep learning framework to build the detection model.
The detection model is planed to be based on `mobilenetv2` with pretrained weights.
