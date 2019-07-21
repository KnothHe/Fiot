from PIL import Image


class ImageOnImage:

    def __init__(self, image, factor=20):
        self.orig_image = image
        self.factor = factor

    def process(self):
        orig_width, orig_height = self.orig_image.size
        scaled_image = self.orig_image.resize((orig_width // self.factor, orig_height // self.factor))
        # create result image
        result_image = Image.new(self.orig_image.mode,
                                 (scaled_image.width * self.factor, scaled_image.height * self.factor),
                                 color=(0, 0, 0))
        # iterator and replace
        block_width, block_height = scaled_image.size
        for w in range(self.factor):
            for h in range(self.factor):
                width_begin = w * block_width
                height_begin = h * block_height
                width_end = width_begin + block_width
                height_end = height_begin + block_height
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


def main():
    infile = "./images/dog.jpg"
    try:
        # open image
        image = Image.open(infile)
        print("Dealing with", infile)
        print("Image size", image.size)
        # process
        result_image = ImageOnImage(image, 20).process()
        result_image.save("image-on-image.jpg")
    except IOError:
        print("Can't open image", infile)


if __name__ == '__main__':
    main()
