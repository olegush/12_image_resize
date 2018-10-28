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


def resize_image(img):
    msgs = [
        'Can not resize the image because too much size parameters.\n',
        'Please check aspect ratio, may be it does not match the original.\n',
        'No parameters for resize.\n',
        'The path is empty or does not exists. '
        'File saved in the current directory.\n',
        'The result file was saved as '
    ]
    msg = ''
    im = Image.open(img.filepath)
    width, height = im.size
    as_ratio = width / height
    if (img.width or img.height) and img.scale:
        return msgs[0]
    elif img.scale:
        newsize = round(width * img.scale), round(height * img.scale)
    elif img.width and img.height:
        msg += msgs[1]
        newsize = img.width, img.height
    elif img.width:
        newsize = int(img.width), round(int(img.width) / as_ratio)
    elif img.height:
        newsize = round(int(img.height) * as_ratio), int(img.height)
    else:
        return msgs[2]
    filename = img.filepath.rsplit('.')[0]
    fileext = img.filepath.rsplit('.')[1]
    imgnew = im.resize(newsize, Image.ANTIALIAS)
    newfilepath = '{}__{}x{}.{}'.format(filename,
                                        str(newsize[0]),
                                        str(newsize[1]),
                                        fileext
                                        )
    if img.output is not None and os.path.isdir(str(img.output)):
        newfilepath = img.output + '/' + newfilepath
    else:
        msg += msgs[3]
    imgnew.save(newfilepath)
    msg += msgs[4] + newfilepath
    return msg


if __name__ == '__main__':
    img = parser_args()
    print(resize_image(img))
