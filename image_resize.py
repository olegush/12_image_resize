import os
import argparse
from PIL import Image


def parser_args():
    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('filepath', help='path to resizing file')
    parser.add_argument('--width', help='width for resize', type=int)
    parser.add_argument('--height', help='height for resize', type=int)
    parser.add_argument('--scale', help='scale for resize', type=float)
    parser.add_argument('--output', help='path to result file')
    args = parser.parse_args()
    return args


def resize_image(filepath, width, height, scale, output):
    msgs = [
        'Please check aspect ratio, may be it does not match the original.\n',
        'The path is empty or not exists. Saved in the current directory.\n',
        'The result file was saved as '
    ]
    msg = ''
    im = Image.open(filepath)
    original_width, original_height = im.size
    as_ratio = original_width / original_height
    if scale:
        newsize = round(original_width * scale), round(original_height * scale)
    elif width and height:
        msg += msgs[0]
        newsize = width, height
    elif width:
        newsize = int(width), round(int(width) / as_ratio)
    else:
        newsize = round(int(height) * as_ratio), int(height)
    filename = filepath.rsplit('.')[0]
    fileext = filepath.rsplit('.')[1]
    imgnew = im.resize(newsize, Image.ANTIALIAS)
    newfilepath = '{}__{}x{}.{}'.format(filename,
                                        str(newsize[0]),
                                        str(newsize[1]),
                                        fileext
                                        )
    if output is not None and os.path.isdir(str(output)):
        newfilepath = output + '/' + newfilepath
    else:
        msg += msgs[1]
    imgnew.save(newfilepath)
    msg += msgs[2] + newfilepath
    return msg


if __name__ == '__main__':
    img = parser_args()
    width = img.width
    height = img.height
    scale = img.scale
    filepath = img.filepath
    output = img.output
    if not(width or height or scale):
        print('No parameters for resize.\n')
    elif (width or height) and scale:
        print('Can not resize the image because too much size parameters.\n')
    else:
        print(resize_image(filepath, width, height, scale, output))
