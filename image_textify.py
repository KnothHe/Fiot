from PIL import Image, ImageFont, ImageDraw
import operator
import argparse
import os


class TextSet:
    def __init__(self, s):
        self.str = str(s)
        self.index = -1

    def next(self):
        self.index = self.index + 1
        if self.index >= len(self.str):
            self.index = 0
        return self.str[self.index]


class ImageTextify:

    def __init__(self, image, font, text="text", text_lines=50, gray=False):
        if gray:
            self.orig_image = image.convert("L")
            self.background_color = 0
        else:
            self.orig_image = image
            self.background_color = (0, 0, 0)
        self.font = font
        self.textSet = TextSet(text)
        self.text_lines = text_lines
        self.gray = gray
        self.orig_width = image.width
        self.orig_height = image.height
        self.mode = self.orig_image.mode

    def setBackgroundColor(self, backgournd_color):
        self.background_color = backgournd_color

    def textify(self):
        # create, scale the image 2 times to anti-aliasing
        zoom_scale = 2
        width = self.orig_width * zoom_scale
        height = self.orig_height * zoom_scale
        block_size = height // self.text_lines
        result_image = Image.new(self.mode, (width, height), self.background_color)
        # font, draw and text
        draw = ImageDraw.Draw(result_image)  # draw on result image
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
                draw.text((block_width, block_height),
                          self.textSet.next(),
                          fill=fill_color,
                          font=font)
        # Zoom out the picture twice as the original image size
        result_image = result_image.resize((width // zoom_scale, height // zoom_scale),
                                           Image.ANTIALIAS)
        return result_image


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
    parser.add_argument('--gray', '-g', dest='gray',
                        type=bool,
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
    # get arguments
    args = parser.parse_args()
    infile = args.infile
    text_lines = args.lines
    text = args.text
    gray = args.gray
    outfile = args.output
    font = args.font
    # process
    if outfile == 'default':
        outfile = './a' + os.path.splitext(infile)[1]
    try:
        # open image
        image = Image.open(infile)
        print("Dealing with", infile)
        print("Image size: ", image.size)
        # textify
        result_image = ImageTextify(image, font, text_lines=text_lines, text=text, gray=gray).textify()
        # save image
        result_image.save(outfile)
        result_image.close()
        print("Saved as", outfile, "\nSize: ", result_image.size, "\n")
    except IOError:
        print("Can't open file:", infile)


if __name__ == "__main__":
    main()
