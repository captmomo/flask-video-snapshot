import operator
import os
import re
from collections import defaultdict
from functools import reduce
from random import choice, randint, shuffle

from nltk import FreqDist
from PIL import Image, ImageChops, ImageOps
from io import BytesIO
import base64

#reference: https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
def PIL_image_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())


def base64_to_PIL_image(base64_img):
    return Image.open(BytesIO(base64.b64decode(base64_img)))

def pixelate_image(img_string):
    image = base64_to_PIL_image(img_string)
    img_data = list(image.getdata())
    freq_dist = FreqDist(img_data)
    top_1_colour = freq_dist.most_common(1)[0][0]
    backgroundColor = top_1_colour
    pixelSize = 9
    image = image.resize(
        (int(image.size[0] / pixelSize), int(image.size[1] / pixelSize)), Image.ANTIALIAS)
    image = image.resize(
        (image.size[0] * pixelSize, image.size[1] * pixelSize), Image.ANTIALIAS)
    pixel = image.load()
    for i in range(0, image.size[0], pixelSize):
        for j in range(0, image.size[1], pixelSize):
            for r in range(pixelSize):
                pixel[i + r, j] = backgroundColor
                pixel[i, j + r] = backgroundColor

    return PIL_image_to_base64(image)


def generate_pixel_image(image_string):
    '''
    https://stackoverflow.com/questions/30520666/pixelate-image-with-pillow

    '''
    block_size = 16
    size = (block_size, block_size)
    image = base64_to_PIL_image(image_string)
    im = image.convert('RGB')
    img_data = list(im.getdata())
    freq_dist = FreqDist(set(img_data))
    most_common = freq_dist.most_common(256)
    palette = []
    for colour in most_common:
        palette.append(colour[0])
    while len(palette) < 256:
        palette.append((0, 0, 0))
    try:
        flat_palette = reduce(lambda a, b: a + b, palette)
        assert len(flat_palette) == 768
        palette_img = Image.new('P', (1, 1), 0)
        palette_img.putpalette(flat_palette)
        multiplier = 8
        scaled_img = im.resize(
            (size[0] * multiplier, size[1] * multiplier), Image.ANTIALIAS)
        reduced_img = scaled_img.quantize(palette=palette_img)
        rgb_img = reduced_img.convert('RGB')
        out = Image.new('RGB', size)
        for x in range(size[0]):
            for y in range(size[1]):
                #sample and get average color in the corresponding square
                histogram = defaultdict(int)
                for x2 in range(x * multiplier, (x + 1) * multiplier):
                    for y2 in range(y * multiplier, (y + 1) * multiplier):
                        histogram[rgb_img.getpixel((x2, y2))] += 1
                color = max(histogram.items(), key=operator.itemgetter(1))[0]
                out.putpixel((x, y), color)

        new_file = ImageOps.scale(out, 50)
        print("pixe_image done")
        output = PIL_image_to_base64(new_file)
    #https://docs.python.org/3/tutorial/errors.html
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        output = image_string
    return output
