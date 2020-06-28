import yaml
import numpy as np
import os
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def load_gt(path):
    with open(path, 'r') as f:
        gts = yaml.load(f, Loader=yaml.CLoader)

    return gts

def save_xml(save_dir, gt, image_name, id, width=640, height=480, channel=3):
    '''

  :param image_name:图片名
  :param gt:对应的bbox
  :param save_dir:
  :param image_name:图片中目标的类别
  :param width:图片的宽度
  :param height:图片的高度
  :param channel:图片的通道
  :return:
  '''

    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'rbg'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '%s' % channel

    node_object = SubElement(node_root, 'object')
    node_name = SubElement(node_object, 'name')
    node_name.text = str(id)
    node_difficult = SubElement(node_object, 'difficult')
    node_difficult.text = '0'

    left, top, right, bottom = gt[0], gt[1], gt[0]+gt[2], gt[1]+gt[3]
    left = int(left)
    top = int(top)
    right = int(right)
    bottom = int(bottom)
    node_bndbox = SubElement(node_object, 'bndbox')
    node_xmin = SubElement(node_bndbox, 'xmin')
    node_xmin.text = '%s' % left
    node_ymin = SubElement(node_bndbox, 'ymin')
    node_ymin.text = '%s' % top
    node_xmax = SubElement(node_bndbox, 'xmax')
    node_xmax.text = '%s' % right
    node_ymax = SubElement(node_bndbox, 'ymax')
    node_ymax.text = '%s' % bottom

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    save_xml = os.path.join(save_dir, image_name.replace('png', 'xml'))
    with open(save_xml, 'wb') as f:
        f.write(xml)

if __name__ == '__main__':
    gtpath = "C:/Users/84517/Desktop/Hinterstoisser/01/gt.yml"
    impath = "C:/Users/84517/Desktop/Hinterstoisser/01/rgb/"
    save_dir='C:/Users/84517/Desktop/Hinterstoisser/01/Annotations/'

    #获得文件中所有图片的文件名
    imname = []
    for root, dirs, files in os.walk(impath, topdown=False):
        for name in files:
            imname.append(name)
        

    #gts是yml文件数据的合集
    gts = load_gt(gtpath)

    #bb是每张照片的bounding box, id是目标类别
    bb = np.empty([len(gts),4])
    id = gts[0][0]['obj_id']

    for i in range(len(gts)):
        bb[i] = gts[i][0]['obj_bb']
        right = bb[i][0]+bb[i][2]
        bottom = bb[i][1]+bb[i][3]


        save_xml(save_dir, bb[i], imname[i], id)
