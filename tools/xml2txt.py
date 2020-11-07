#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob, shutil
import xml.etree.ElementTree as ET
from PIL import Image


CATEGORIES = ['l_sleeve', 's_sleeve', 'unsure_up', 'trousers', 'shorts', 'unsure_down']


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' %(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' %(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xmls, save_dir):
    for xml_f in xmls:
        img_f = xml_f.replace('.xml', '.jpg')
        img_w, img_h = Image.open(img_f).size

        name = xml_f.split('/')[-1][:-4]
        print("Processing %s" % name)
        tree = ET.parse(xml_f)
        root = tree.getroot()

        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        assert (width == img_w) & (height == img_h)

        f = open(os.path.join(save_dir, name+'.txt'), 'w')
        for obj in get(root, 'object'):
            categories = obj.findall('class')
            if len(categories) == 0:
                continue
            categories = [cate.text for cate in categories]
            # print('before: ', categories)
            if 'unsure' in categories:
                idx = categories.index('unsure')
                if 'l_sleeve' in categories or 's_sleeve' in categories:
                    categories[idx] = 'unsure_down'
                elif 'trousers' in categories or 'shorts' in categories:
                    categories[idx] = 'unsure_up'
                else:
                    categories = ['unsure_up', 'unsure_down']
            if len(categories) == 1:
                if 'l_sleeve' in categories or 's_sleeve' in categories:
                    categories.append('unsure_down')
                else:
                    categories.append('unsure_up')
            # print('after: ', categories)

            category_id = sorted([CATEGORIES.index(cate) for cate in categories])
            print(category_id)
            assert len(category_id) == 2

            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = float(get_and_check(bndbox, 'xmin', 1).text)
            ymin = float(get_and_check(bndbox, 'ymin', 1).text)
            xmax = float(get_and_check(bndbox, 'xmax', 1).text)
            ymax = float(get_and_check(bndbox, 'ymax', 1).text)
            assert(xmax > xmin) & (ymax > ymin)
            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2
            o_width = xmax - xmin
            o_height = ymax - ymin
            x_center = round(x_center / width, 6)
            y_center = round(y_center / height, 6)
            o_width = round(o_width / width, 6)
            o_height = round(o_height / height, 6)
            category_id = ','.join(map(str, category_id))
            coord = map(str, [x_center, y_center, o_width, o_height])
            f.write(category_id + ' ' + ' '.join(coord))
            f.write('\n')
        f.close()


if __name__ == '__main__':
    root = '/Users/dyy/Desktop/clothes'
    # xmls = sorted(glob.glob(os.path.join(root, '*.xml')))
    # convert(xmls, root)
    imgs = glob.glob(os.path.join(root, '*.txt'))
    save_dir = '/Users/dyy/Desktop/train'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for img in imgs:
        name = img.split('/')[-1]
        shutil.copy(img, os.path.join(save_dir, name))

