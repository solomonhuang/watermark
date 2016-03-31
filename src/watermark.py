# -*- coding:utf-8 -*-
import argparse
from PIL import Image

def roll_mask(image, mask_size):
    mask_xsize, mask_ysize = mask_size

    image = image.convert("RGBA")
    datas = image.getdata()
    newDatas = []
    for item in datas:
        if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
            newDatas.append((255,255,255,0))
        else:
            newDatas.append((item[0], item[1], item[2], 50))

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


outfile = "result.jpg"
mask = Image.open("mask.jpg")
target = Image.open("target.jpg")
target = target.convert("RGBA")
mask = roll_mask(mask, target.size)
im = Image.alpha_composite(target, mask)
im.save(outfile)
