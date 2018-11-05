import os
import argparse
from PIL import Image


def get_args_parser():
    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('filepath', help='path to resizing file')
    parser.add_argument('--width', help='width for resize', type=int)
    parser.add_argument('--height', help='height for resize', type=int)
    parser.add_argument('--scale', help='scale for resize', type=float)
    parser.add_argument('--output', help='path to directory for result file')
    return parser


def validate_args(filepath, width, height, scale, parser):
    if not os.path.isfile(filepath):
        parser.error('File not found')
    if not(width or height or scale):
        parser.error('No parameters for resize')
    if (width or height) and scale:
        parser.error('Can not resize, too much resize parameters')
    if width == 0 or height == 0 or scale == 0:
        parser.error('Can not resize, some parameters equal to zero.\n')
    if width and width < 0 or height and height < 0 or scale and scale < 0:
        parser.error('Can not resize, some parameters less than zero.\n')


def calc_new_size(orig_width, orig_height, width, height, scale, as_ratio):
    if scale:
        new_size = round(orig_width * scale), round(orig_height * scale)
    elif width and height:
        new_size = width, height
    elif width:
        new_size = width, round(width / as_ratio)
    else:
        new_size = round(height * as_ratio), height
    return new_size


def resize_image(img_obj, new_size):
    return img_obj.resize(new_size, Image.ANTIALIAS)


def make_name(full_filename, new_size):
    file_name, file_ext = os.path.splitext(full_filename)
    new_width, new_height = new_size
    return '{}__{}x{}{}'.format(
        file_name,
        new_width,
        new_height,
        file_ext
    )


if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    width = args.width
    height = args.height
    scale = args.scale
    filepath = args.filepath
    output = args.output
    validate_args(filepath, width, height, scale, parser)
    print('\nImage Resizer Log:')
    img_obj = Image.open(filepath)
    orig_width, orig_height = img_obj.size
    as_ratio = round(orig_width / orig_height, 1)
    new_size = calc_new_size(orig_width, orig_height, width, height, scale,
                             as_ratio
                             )
    if as_ratio != round(new_size[0] / new_size[1], 1):
        print('- aspect ratio does not match the original.')
    img_new_obj = resize_image(img_obj, new_size)
    dirpath, full_filename = os.path.split(filepath)
    new_full_filename = make_name(full_filename, new_size)
    if output and os.path.isdir(output):
        new_filepath = os.path.join(output, new_full_filename)
    else:
        new_filepath = os.path.join(dirpath, new_full_filename)
        print('- the path is not exists, will be save in the same dir.')
    img_new_obj.save(new_filepath)
    print('- the result file was saved.')
