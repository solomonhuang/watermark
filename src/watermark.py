# -*- coding:utf-8 -*-
import os
import argparse
from PIL import Image

def roll_mask(image, mask_size, alpha=0.2):
    mask_xsize, mask_ysize = mask_size

    image = image.convert("RGBA")
    datas = image.getdata()
    newDatas = []
    for item in datas:
        if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
            newDatas.append((item[0], item[1], item[2],0))
        else:
            newDatas.append((item[0], item[1], item[2], int(255*alpha)))

    image.putdata(newDatas)

    xsize, ysize = image.size
    size = xsize > ysize and xsize or ysize
    size = mask_xsize > size and mask_xsize or size
    size = mask_ysize > size and mask_ysize or size
    size = size * 2
    im = Image.new("RGBA", (size, size))
    for y in range(0, size, ysize):
        for x in range(0, size, xsize):
            im.paste(image, (x, y, x+xsize, y+ysize))

    im = im.rotate(45)
    crop_left = int((size-xsize)/2)
    crop_top = int((size-ysize)/2)
    crop_right = crop_left + mask_xsize
    crop_bot = crop_top + mask_ysize
    im = im.crop((crop_left, crop_top, crop_right, crop_bot))
    return im

parser = argparse.ArgumentParser(prog="watermark",
                                 description="Watermark: add watermark on images")

parser.add_argument('-m', type=str, help="Watermark picture", required=True)
parser.add_argument('-i', type=str, help="Target picture", required=True)
parser.add_argument('-t', type=float, help="Watermark transparent value(default: 0.2)", default=.2)
parser.add_argument('-d', type=str, help="Result director", default="results")

#parser.print_help()
args = parser.parse_args()
#print(args.i)
#print(args.m)
#print(args.t)
#print(args.d)

try:
    os.mkdir(args.d)
except:
    pass

outfile = args.d + os.sep + os.path.basename(args.i)

mask = Image.open(args.m)
target = Image.open(args.i)
target = target.convert("RGBA")
mask = roll_mask(mask, target.size, args.t)
im = Image.alpha_composite(target, mask)
im.save(outfile)
