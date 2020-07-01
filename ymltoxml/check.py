import yaml
import numpy as np
import os
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def load_gt(path):
    with open(path, 'r') as f:
        gts = yaml.load(f, Loader=yaml.CLoader)

    return gts


if __name__ == '__main__':
    gtpath = "C:/Users/84517/Desktop/Hinterstoisser/15/gt.yml"

    #gts是yml文件数据的合集
    gts = load_gt(gtpath)

    #bb是每张照片的bounding box, id是目标类别
    bb = np.empty([len(gts),4])


    for i in range(len(gts)):
        bb[i] = gts[i][0]['obj_bb']
        right = bb[i][0]+bb[i][2]
        bottom = bb[i][1]+bb[i][3]

        if bb[i][0] < 1:
            print(i)
        if bb[i][1] < 1:
            print(i)
        if right > 639:
            print(i)
        if bottom > 479:
            print(i)
            

