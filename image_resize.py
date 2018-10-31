import os
import argparse
from PIL import Image


def parser_args():
    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('filepath', help='path to resizing file')
    parser.add_argument('--width', help='width for resize', type=int)
    parser.add_argument('--height', help='height for resize', type=int)
    parser.add_argument('--scale', help='scale for resize', type=float)
    parser.add_argument('--output', help='path to directory for result file')
    args = parser.parse_args()
    return args


def resize_msgs(message_type):
    msgs = {
        'ratio': 'Aspect ratio does not match the original.\n',
        'output': 'The path is not exists. Saved in the current dir.\n',
        'final': 'The result file was saved in the output dir '
    }
    print(msgs[message_type])


def resize_image(filepath, width, height, scale, output):
    im = Image.open(filepath)
    original_width, original_height = im.size
    as_ratio = round(original_width / original_height, 2)
    if scale:
        newsize = round(original_width * scale), round(original_height * scale)
    elif width and height:
        newsize = width, height
        if as_ratio != round(width/height, 2):
            resize_msgs('ratio')
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
    if output and os.path.isdir(output):
        newfilepath = os.path.join(output, newfilepath)
    else:
        resize_msgs('output')
    imgnew.save(newfilepath)
    resize_msgs('final')
    return True


if __name__ == '__main__':
    args_img = parser_args()
    width = args_img.width
    height = args_img.height
    scale = args_img.scale
    filepath = args_img.filepath
    output = args_img.output
    if not os.path.isfile(filepath):
        exit('No such file')
    if not(width or height or scale):
        exit('No parameters for resize.\n')
    elif (width or height) and scale:
        exit('Can not resize the image because too much size parameters.\n')
    else:
        resize_image(filepath, width, height, scale, output)
