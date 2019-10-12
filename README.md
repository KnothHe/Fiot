# Fiot

Fill image with other things

A simple program that replaces the original pixels of a picture with other things

## Prerequisites

### Dependencies

Python interpreter and package Pillow.

#### Install `Pillow`

```bash
pip install Pillow
```

## Run

```bash
python porg.py image
```

## Usage

~~~
python fiot.py -h
~~~

- Fill image with text
~~~
python fiot.py fit -h
~~~
or
~~~
python fit.py -h
~~~

- Fill image with image[s]
~~~
python fiot.py fii -h
~~~
or
~~~
python fii.py -h
~~~

## Result

[Test image source](https://unsplash.com/photos/sirEpWjfSmo)

- Original image:
![original image](./images/dog-test01.jpg)

- Image filled with text (50x50):
![textify image](./images/dog-filled-with-text.jpg)

- Image filled with itself (20x20):
![image filled with itself](./images/dog-image-on-image.jpg)

- Image filled with other image (10x10):
![image filled with other image](./images/dog-filled-with-other-image.jpg)

- Image filled with images include itself (10x10):
![image filled with images include itself](./images/dog-filled-with-images-include-itself.jpg)

## Note

Because I want to use CJK text,
I have set a font that supports CJK text Under the font directory.

You could specify the font to use, if the default font is not displayed

## TODO

- [x] image on image (fii) command line parser
- [x] combine two programs, though it is very ugly now
- [ ] add set background color argument
- [ ] add whether loop text argument

## License

Though it is so tiny and may not good, it still has a licence.

The project is released under the MIT License.

## Off topic

I don't know much about Python, so the code may not be very good.

At the same time, I am not sure whether the use of Noto font is infringing.
If so, please let me know and I will delete it.
