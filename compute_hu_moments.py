#!/usr/bin/env python2

import cv2 as cv
import numpy as np
import glob, os
from sys import argv

kx = 0.1
kx2 = 1 - kx
def boundingRect_sel (rect, img_shape):
    x, y, sw, sh = rect
    h, w = img_shape
    if ((kx * w < x) and (kx * h < y) and
        (kx2 * w > (x + sw)) and ((y + sh) < kx2 * h)):
        return True

    return False

lenk = 1.0
def contours_selection(cnts, img_shape):
    w, h = img_shape
    minl = lenk/2 * np.sqrt(w * w + h * h)
    for i in xrange(0, len(cnts)):
        if ((minl < cv.arcLength(cnts[i], True)) and
            boundingRect_sel(cv.boundingRect(cnts[i]), img_shape)):
            return i

    return None # len(cnts) - 1

def parse_file_metadata(f):
    nam = os.path.splitext(os.path.basename(f))[0]
    l = nam.split('.')

    obj = l[0]
    ops = 'none'
    wid = 0

    if len(l) == 3:
        ops = l[1]
        wid = int(l[2])
    else:
        wid = int(l[1])

    return obj, ops, wid


def contour_data_record(f, cnt):
    obj, ops, wid = parse_file_metadata(f)
    moments = cv.HuMoments(cv.moments(cnt))
    line = "{:>18} {:>4}".format(obj, str(wid))
    for m in moments:
        line += " {:>20.8e}".format(m[0])
    line += " {:<}".format(ops)
    return line

def marked_file (path):
    des, file = os.path.split(path)
    return des + "/marked/" + file

def handle_file (path):
    img = cv.cvtColor(cv.imread(path), cv.COLOR_RGB2GRAY)
    img[img < 255] = 0
    cnts, h =cv.findContours(img,
                             cv.RETR_LIST,
                             cv.CHAIN_APPROX_NONE)
    ci = contours_selection(cnts, img.shape)


    if ci is not None:
        img = cv.imread(path)
        cv.drawContours(img, cnts, ci,
                        (112,181,27),
                        thickness = 2)
        cv.imwrite(marked_file(path), img)

        print(contour_data_record(path, cnts[ci]))

if __name__ == "__main__":
    for p in glob.glob("./tmp/*.png"):
        handle_file(p)

