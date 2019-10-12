#!/bin/python3
from PIL import Image, ImageFont, ImageDraw
import operator
import argparse
import os
import sys


class TextSet:
    def __init__(self, s, loop):
        self.str = str(s)
        self.index = -1
        self.loop = loop

    def next(self):
        self.index = self.index + 1
        if self.index >= len(self.str):
            if not self.loop:
                raise Exception('The text is used up')
            self.index = 0
        return self.str[self.index]


class ImageTextify:

    def __init__(self, image, font, text="text", text_lines=50, gray=False, loop=True):
        if gray:
            self.orig_image = image.convert("L")
            self.background_color = 0
        else:
            self.orig_image = image
            self.background_color = (0, 0, 0)
        self.font = font
        self.textSet = TextSet(text, loop)
        self.text_lines = text_lines
        self.gray = gray
        self.orig_width = image.width
        self.orig_height = image.height
        self.mode = self.orig_image.mode
        self.zoom_scale = 2
        self.width = self.orig_width * self.zoom_scale
        self.height = self.orig_height * self.zoom_scale
        self.block_size = self.height // self.text_lines

    def setBackgroundColor(self, backgournd_color):
        self.background_color = backgournd_color

    def replace(self, image):
        zoom_scale = self.zoom_scale
        width = self.width
        height = self.height
        block_size = height // self.text_lines
        # font, draw and text
        draw = ImageDraw.Draw(image)  # draw on result image
        font = ImageFont.truetype(self.font, block_size)  # font used
        # iterator and replace
        for h in range(0, height // block_size):
            for w in range(0, width // block_size):
                block_width = w * block_size
                block_height = h * block_size
                # initialize fill color
                if self.gray:
                    fill_color = 0
                else:
                    fill_color = (0, 0, 0)
                # get average color in the block
                width_begin = max(0, block_width)
                width_end = min(width, block_width + block_size)
                height_begin = max(0, block_height)
                height_end = min(height, block_height + block_size)
                for i in range(block_width, block_width + block_size):
                    for j in range(block_height, block_height + block_size):
                        pixel = self.orig_image.getpixel((i / zoom_scale, j / zoom_scale))
                        if self.gray:
                            fill_color = fill_color + pixel
                        else:
                            fill_color = tuple(map(operator.add, fill_color, pixel))
                block_area = (width_end - width_begin) * (height_end - height_begin)
                if self.gray:
                    fill_color = fill_color // block_area
                else:
                    fill_color = tuple(x // block_area for x in fill_color)
                # draw text on the result image
                try:
                    text = self.textSet.next()
                    draw.text((block_width, block_height),
                              text,
                              fill=fill_color,
                              font=font)
                except Exception as inst:
                    return image
        return image

    def textify(self):
        # create, scale the image 2 times to anti-aliasing
        zoom_scale = self.zoom_scale
        width = self.width
        height = self.height
        result_image = Image.new(self.mode, (width, height), self.background_color)
        # replace original pixel with text
        result_image = self.replace(result_image)
        # Zoom out the picture twice as the original image size
        result_image = result_image.resize((width // zoom_scale, height // zoom_scale),
                                           Image.ANTIALIAS)
        return result_image


def isColorString(color):
    if len(color) != 6:
        return False
    try:
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    except ValueError:
        return False
    if r < 0 or r >= 256 or g < 0 or g >= 256 or b < 0 or b >= 256:
        return False
    return True


def main():
    # create parser
    parser = argparse.ArgumentParser(description="A simple program that"
                                                 " replaces the original "
                                                 "pixels of a picture with text")
    # add arguments
    parser.add_argument('infile', metavar='input',
                        type=str,
                        help='input file')
    parser.add_argument('--lines', '-l', dest='lines',
                        type=int,
                        default=50,
                        help='text lines will on the image, default: 50')
    parser.add_argument('--text', '-t', dest='text',
                        default='text',
                        help='text will be drawn on the image, default: text')
    parser.add_argument('--gray', '-g', dest='gray', nargs='?',
                        type=bool,
                        const=True,
                        default=False,
                        help='whether to output grayscale image, default: False')
    parser.add_argument('--output', '-o', dest='output',
                        type=str,
                        default='default',
                        help='output file path, default: ./a.extension')
    parser.add_argument('--font', '-f', dest='font',
                        type=str,
                        default='./font/NotoSansCJK-Regular.ttc',
                        help='specify the font to use, if the default font is not displayed')
    parser.add_argument('--background-color', '-b', dest='background_color',
                        type=str,
                        default='000000',
                        help='specify the background color in hex format when gray is not set '
                             'and in int format when gray is set. '
                             'when use int format, the range of color is 0 - 255 '
                             'In hex format e.g. 00ff00. '
                             'In int format e.g. 0')
    parser.add_argument('--not-loop-text', '-n', dest='loop_text', nargs='?',
                        type=bool,
                        const=False,
                        default=True,
                        help='whether to loop text when the text is used up')
    # get arguments
    args = parser.parse_args()
    infile = args.infile
    text_lines = args.lines
    text = args.text
    gray = args.gray
    outfile = args.output
    font = args.font
    background_color = args.background_color
    loop_text = args.loop_text
    if not gray:
        if not isColorString(background_color):
            sys.exit("background color format is wrong.")
        r, g, b = int(background_color[0:2], 16), int(background_color[2:4], 16), int(background_color[4:6], 16)
        background_color = (r, g, b)
    else:
        try:
            if background_color == '000000':
                background_color = 0
            else:
                background_color = int(background_color)
            if background_color < 0 or background_color >= 256:
                raise ValueError
        except ValueError:
            sys.exit("background color format is wrong.")
    # process
    if outfile == 'default':
        outfile = './a' + os.path.splitext(infile)[1]
    try:
        # open image
        image = Image.open(infile)
        print("Dealing with", infile)
        print("Image size: ", image.size)
        # textify
        image_textify = ImageTextify(image, font, text_lines=text_lines, text=text, gray=gray, loop=loop_text)
        image_textify.setBackgroundColor(background_color)
        result_image = image_textify.textify()
        # save image
        result_image.save(outfile)
        result_image.close()
        print("Saved as", outfile, "\nSize: ", result_image.size, "\n")
    except IOError:
        print("Can't open file:", infile)


if __name__ == "__main__":
    main()
