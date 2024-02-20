# create images for okn animation

import argparse
import contextlib
import cv2
import glob
import math
import numpy as np
import os
from PIL import Image
import shutil
import sys

def create_gif(framedir: str, outfile: str, duration_ms: int) -> None:
    # from https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    with contextlib.ExitStack() as stack:
        # load frames
        frames = (stack.enter_context(Image.open(f))
                  for f in sorted(glob.glob(os.path.join(framedir, "*.png"))))

        frame = next(frames)

        frame.save(fp=outfile, format="GIF", append_images=frames,
                   save_all=True, duration=duration_ms, loop=0)

    return

def create_okn_frame(width: int, height: int, line_width: int,
                     offset: int, outfile: str) -> None:
    canvas = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)

    num_bars = math.ceil((width - offset) / line_width)
    for i in range(-1, num_bars, 2):
        x_start = offset + (i * line_width)
        x_finish = min(width, x_start + line_width)

        if x_finish < 0:
            continue

        cv2.rectangle(canvas, (max(0, x_start), 0), (x_finish, height), (0, 0, 0), -1)

    cv2.imwrite(outfile, canvas)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    description="Generate images for OKN animation"
                )
    parser.add_argument("--width_px", type=int, default=800)
    parser.add_argument("--height_px", type=int, default=600)
    parser.add_argument("--line_width_px", type=int, default=54) # default 20 bars
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--overwrite", action="store_true", default=False)
    parser.add_argument("--output_gif", type=str, default="okn.gif")
    parser.add_argument("--duration_ms", type=int, default=1)
    parser.add_argument("--step_px", type=int, default=2)
    args = parser.parse_args()

    # validate command line args
    if os.path.exists(args.output_dir):
        if args.overwrite:
            print("Overwriting directory:", args.output_dir)
            shutil.rmtree(args.output_dir)
        else:
            print("ERROR: output directory exists! Hint: use --overwrite", file=sys.stderr)
            sys.exit(1)

    os.makedirs(args.output_dir)

    # create the frames
    for offset in range(1, args.line_width_px * 2, args.step_px):
        outfile = os.path.join(args.output_dir, "okn_frame_" + str(offset).zfill(4) + ".png")
        create_okn_frame(args.width_px, args.height_px, args.line_width_px,
                         offset, outfile)

    # create the gif
    create_gif(args.output_dir, args.output_gif, args.duration_ms)

    print("All done! Have a nice day :)")

# EOF
