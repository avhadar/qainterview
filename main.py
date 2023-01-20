import argparse
import copy
import csv
import os
import time
import cv2


class PixelFilter:

    def __init__(self, name, specs):
        self.__name = name
        self.__specs = specs

    def get_name(self):
        return self.__name

    def apply(self, pixel):
        __pixel = copy.copy(pixel)
        h = pixel[0]
        __wavelength = self.convert_hue_to_wavelength(h)
        for spec in self.__specs:
            if spec['wavelength_in'] == __wavelength:
                h = self.convert_wavelength_to_hue(spec['wavelength_out'])
                s = pixel[1]
                v = int(pixel[2] * spec['intensity_out'])
                __pixel = (h, s, v)

        return __pixel

    def convert_hue_to_wavelength(self, hue):
        return 650 - hue*int(250/270.0)

    def convert_wavelength_to_hue(self, wavelength):
        hue = int(270/250)*(650-wavelength)
        hue = min(hue, 255)
        hue = max(hue, 0)
        return hue


def iterate(filter_idx, input, filter, verbose=False):

    raw_image = cv2.imread(input)
    height, width, depth = raw_image.shape

    filtered_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV)

    last_progress = 0
    for i in range(height):
        for j in range(width):
            hsv_pixel = filtered_image[i, j]
            new_pixel = filter.apply(hsv_pixel)
            pixel = new_pixel
            filtered_image[i, j] = pixel
            progress = 100*((i+1)*width+(j+1))/(width*height)
            if verbose and int(progress) > int(last_progress)+4:
                print('Processing %s: %s with filter: %s. Status: %3d' % (filter_idx, args.input, filter.get_name(), progress) + "%.")
                last_progress = int(progress)

    filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_HSV2BGR)
    return raw_image, filtered_image


def get_filter(filter):
    spec = []
    with open(filter, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['wavelength_in'] = int(row['wavelength_in'])
            row['wavelength_out'] = int(row['wavelength_out'])
            row['intensity_out'] = float(row['intensity_out'])/100.0
            spec.append(row)

    return PixelFilter(filter, spec)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Render a filtered image.')
    parser.add_argument('-i', dest='input', action='store', help='Specify the input file')
    parser.add_argument('-f', dest='filters', action='append', help='Specify the filter spec filepath.')
    parser.add_argument('-o', dest='output', action='store', help='Specify the output file.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Specify the output file.')

    args = parser.parse_args()
    input = args.input
    output = args.output
    filters = args.filters

    os.environ['TERM'] = 'xterm'

    if args.verbose:
        os.environ['VERBOSE'] = "true"
    else:
        os.environ.setdefault('VERBOSE', "false")

    begin_time = time.time()
    for filter_idx, filter in enumerate(filters):
        print('Processing %d/%d: %s with filter: %s. Status:   0%s.' % (filter_idx+1, filters.__len__(), args.input, filter, "%"))
        raw_image, filtered_image = iterate("%d/%d" % (filter_idx+1, filters.__len__()), input, get_filter(filter), 'VERBOSE' in os.environ)
        input = filtered_image
    end_time = time.time()

    duration = int(end_time-begin_time)
    print('Duration: %s seconds.' % duration)

    cv2.imwrite(output, filtered_image)
