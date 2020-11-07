#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
import json
import shutil
import xml.etree.ElementTree as ET


START_IMAGE_ID = 1
START_BOUNDING_BOX_ID = 1
PRE_DEFINE_CATEGORIES = {'l_sleeve': 1, 'trousers': 2, 's_sleeve': 3, 'shorts': 4, 'unsure': 5}

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


def convert(xmls, save_json):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    image_id = START_IMAGE_ID
    for xml_f in xmls:
        name = xml_f.split('/')[-1][:-4]
        print("Processing %s" % name)
        tree = ET.parse(xml_f)
        root = tree.getroot()

        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': name+'.jpg', 'height': height, 'width': width, 'id': image_id}
        json_dict['images'].append(image)

        for obj in get(root, 'object'):
            # category = get_and_check(obj, 'name', 1).text
            # category_id = categories[category]
            category = obj.findall('class')
            # category_id = [categories[cate.text] for cate in category]
            for cate in category:
                category_id = categories[cate.text]

                bndbox = get_and_check(obj, 'bndbox', 1)
                xmin = float(get_and_check(bndbox, 'xmin', 1).text)
                ymin = float(get_and_check(bndbox, 'ymin', 1).text)
                xmax = float(get_and_check(bndbox, 'xmax', 1).text)
                ymax = float(get_and_check(bndbox, 'ymax', 1).text)
                assert(xmax > xmin)
                assert(ymax > ymin)
                o_width = abs(xmax - xmin)
                o_height = abs(ymax - ymin)
                ann = {'area': o_width*o_height, 'iscrowd': 0, 'image_id': image_id,
                       'bbox': [xmin, ymin, o_width, o_height],
                       'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                       'segmentation': []}
                json_dict['annotations'].append(ann)
                bnd_id += 1
        image_id += 1

    categories = sorted(categories.items(), key=lambda x: x[1])
    for cate, cid in categories:
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)

    json_fp = open(save_json, 'w')
    json_str = json.dumps(json_dict, indent=4)
    json_fp.write(json_str)
    json_fp.close()


if __name__ == '__main__':
    root = '/Users/dyy/Desktop/test'
    xmls = glob.glob(os.path.join(root, '*.xml'))
    convert(xmls, save_json=os.path.join(root, 'all.json'))


