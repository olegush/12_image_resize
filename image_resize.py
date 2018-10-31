import os
import argparse
from PIL import Image


def open_img(filepath):
    return Image.open(filepath)


def get_args_parser():
    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('filepath', help='path to resizing file')
    parser.add_argument('--width', help='width for resize', type=int)
    parser.add_argument('--height', help='height for resize', type=int)
    parser.add_argument('--scale', help='scale for resize', type=float)
    parser.add_argument('--output', help='path to directory for result file')
    args = parser.parse_args()
    return args


def print_messages(message_type):
    msgs = {
        'ratio': 'Aspect ratio does not match the original.\n',
        'output': 'The path is not exists, will be save in the current dir.\n',
        'final': 'The result file was saved.'
    }
    print(msgs[message_type])


def calc_newsize(img_obj, width, height, scale):
    original_width, original_height = img_obj.size
    as_ratio = round(original_width / original_height, 2)
    if scale:
        newsize = round(original_width * scale), round(original_height * scale)
    elif width and height:
        newsize = width, height
        if as_ratio != round(width/height, 2):
            print_messages('ratio')
    elif width:
        newsize = int(width), round(int(width) / as_ratio)
    else:
        newsize = round(int(height) * as_ratio), int(height)
    return newsize


def resize_image(img_obj, newsize):
    return img_obj.resize(newsize, Image.ANTIALIAS)


def give_path(filepath, newsize, output):
    filename = filepath.rsplit('.')[0]
    fileext = filepath.rsplit('.')[1]
    newwidth = str(newsize[0])
    newheight = str(newsize[1])
    newfilepath = '{}__{}x{}.{}'.format(filename, newwidth, newheight, fileext)
    if output and os.path.isdir(output):
        newfilepath = os.path.join(output, newfilepath)
    else:
        print_messages('output')
    return newfilepath


def save_img(imgnew_obj, filepath):
    imgnew_obj.save(filepath)
    print_messages('final')


if __name__ == '__main__':
    args_img = get_args_parser()
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
        img_obj = open_img(filepath)
        newsize = calc_newsize(img_obj, width, height, scale)
        imgnew_obj = resize_image(img_obj, newsize)
        newpath = give_path(filepath, newsize, output)
        save_img(imgnew_obj, newpath)
