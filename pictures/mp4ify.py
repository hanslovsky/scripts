#!/usr/bin/env python3

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('images', nargs='+', type=Path)
parser.add_argument('--output', '-o', type=Path, required=True)
parser.add_argument('--frame-rate', '-f', type=float, required=False, default=5)
args = parser.parse_args()

# Calculate the duration per frame
frame_duration_ms = round(1000 / args.frame_rate) # milliseconds

# Load each frame as a PIL.Image object and store it in a list
frames = [np.asarray(Image.open(image)) for image in args.images]
# Save the first frame as the output image, with all remaining frames appended

video = cv2.VideoWriter(
    str(args.output),
    cv2.VideoWriter_fourcc(*'mp4v'),  # -1,  # manual codec selection
    args.frame_rate,
    frames[0].shape[:2][::-1]  # width and height
)

try:
    for frame in frames:
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

except Exception as e:
    print(f'Failed: {e}')
    video.release()

