#!/bin/python3
from PIL import Image
import argparse
import os
import sys


class ImageSet:

    def __init__(self, images):
        self.images = images
        self.index = -1

    def next(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        return self.images[self.index]


class ImageOnImage:

    def __init__(self, images, factor=20, include_self=True):
        self.orig_image = images[0]
        if not include_self and len(images) > 1:
            images = images[1:]
        self.factor = factor
        scaled_width, scaled_height = [s // factor for s in list(images[0].size)]
        scaled_images = []
        for img in images:
            scaled_images.append(img.resize((scaled_width, scaled_height)))
        self.image_set = ImageSet(scaled_images)

    def process(self):
        image_set = self.image_set
        orig_width, orig_height = self.orig_image.size
        scaled_image = self.orig_image.resize((orig_width // self.factor, orig_height // self.factor))
        # create result image
        result_image = Image.new(self.orig_image.mode,
                                 (scaled_image.width * self.factor, scaled_image.height * self.factor),
                                 color=(0, 0, 0))
        # iterator and replace
        block_width, block_height = scaled_image.size
        for h in range(self.factor):
            for w in range(self.factor):
                width_begin = w * block_width
                height_begin = h * block_height
                width_end = width_begin + block_width
                height_end = height_begin + block_height
                scaled_image = image_set.next()
                for i in range(width_begin, width_end):
                    for j in range(height_begin, height_end):
                        color = scaled_image.getpixel((i % block_width, j % block_height))
                        orig_color = self.orig_image.getpixel((i, j))
                        result_color = []
                        for c in range(3):
                            result_color.append((orig_color[c] + color[c]) // 2)
                        # print(color)
                        result_image.putpixel((i, j), tuple(result_color))

        return result_image


def test():
    infiles = ["./images/dog-test01.jpg", "./images/dog-test02.jpg"]
    try:
        # open image
        images = []
        for file in infiles:
            images.append(Image.open(file))
        print("Dealing with", infiles)
        print("Image size", images[0].size)
        # process
        result_image = ImageOnImage(images, 10, include_self=True).process()
        result_image.save("image-on-image.jpg")
    except IOError:
        print("Can't open files:", infiles)


def main():
    # create parser
    parser = argparse.ArgumentParser(description="A simple program that"
                                                 " replaces the original "
                                                 "pixels of a picture with image[s]")
    # add arguments
    parser.add_argument('infiles', metavar='input',
                        type=str,
                        nargs="+",
                        help='input files, at least one file')
    parser.add_argument('--factor', '-f', dest='factor',
                        type=int,
                        default=20,
                        help='text lines will on the image, default: 20')
    parser.add_argument('--include_self', '-i', dest='include_self',
                        type=bool,
                        default=False,
                        help='whether to include the output image as background, '
                             'default: not include. However if just one image as input'
                             'this value must be True')
    parser.add_argument('--output', '-o', dest='output',
                        type=str,
                        default='default',
                        help='output file path, default: ./a.extension')

    # get arguments
    args = parser.parse_args()
    infiles = args.infiles
    factor = args.factor
    include_self = args.include_self
    outfile = args.output

    # process
    if outfile == 'default':
        outfile = './a' + os.path.splitext(infiles[0])[1]
    try:
        # open image
        images = []
        for file in infiles:
            images.append(Image.open(file))
        print("Dealing with", infiles[0])
        print("Image size: ", images[0].size)
        # process image
        result_image = ImageOnImage(images=images, factor=factor, include_self=include_self).process()
        # save image
        result_image.save(outfile)
        result_image.close()
        print("Saved as", outfile, "\nSize: ", result_image.size, "\n")
    except IOError:
        print("Can't open files:", infiles)


if __name__ == '__main__':
    main()
