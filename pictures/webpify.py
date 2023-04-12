#!/usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('images', nargs='+', type=Path)
parser.add_argument('--output', '-o', type=Path, required=True)
parser.add_argument('--frame-rate', '-f', type=float, required=False, default=5)
parser.add_argument('--lossless', action='store_true', required=False)
parser.add_argument('--method', '-m', type=int, required=False, default=6)
args = parser.parse_args()

# Calculate the duration per frame
frame_duration_ms = round(1000 / args.frame_rate) # milliseconds

# Load each frame as a PIL.Image object and store it in a list
frames = [Image.open(image) for image in args.images]
# Save the first frame as the output image, with all remaining frames appended
frames[0].save(
    args.output,
    "webp",
    lossless=args.lossless,
    method=args.method,
    append_images=frames[1:],
    duration=frame_duration_ms,
    save_all=True
)
