import os
import shutil
import glob
import random
from xml2txt import convert

print('start processing dataset...')
ori_data_path = '/home/data'
train_ratio = 0.9
save_path = '/project/train/preprocessed_dataset/yolo/'
if os.path.exists(save_path):
    shutil.rmtree(save_path)
os.makedirs(save_path)

images = glob.glob(os.path.join(ori_data_path, '*/*.jpg'))
total = len(images)
if train_ratio < 1:
    train_num = int(train_ratio * total)
    random.shuffle(images)
    train_images = random.sample(images, train_num)
    val_images = list(set(images) - set(train_images))
else:
    train_images = images
    val_images = []

if not os.path.exists(os.path.join(save_path, 'images/train')):
    os.makedirs(os.path.join(save_path, 'images/train'))
if not os.path.exists(os.path.join(save_path, 'images/val')):
    os.makedirs(os.path.join(save_path, 'images/val'))
if not os.path.exists(os.path.join(save_path, 'labels/train')):
    os.makedirs(os.path.join(save_path, 'labels/train'))
if not os.path.exists(os.path.join(save_path, 'labels/val')):
    os.makedirs(os.path.join(save_path, 'labels/val'))

for img in train_images:
    ann = img.replace('jpg', 'xml')
    img_name = os.path.split(img)[-1]
    ann_name = os.path.split(ann)[-1]
    shutil.copy(img, os.path.join(save_path, 'images/train', img_name))
    shutil.copy(ann, os.path.join(save_path, 'images/train', ann_name))

for img in val_images:
    ann = img.replace('jpg', 'xml')
    img_name = os.path.split(img)[-1]
    ann_name = os.path.split(ann)[-1]
    shutil.copy(img, os.path.join(save_path, 'images/val', img_name))
    shutil.copy(ann, os.path.join(save_path, 'images/val', ann_name))

for phase in ('train', 'val'):
    ann_dir = save_path + 'images/' + phase
    save_dir = save_path + 'labels/' + phase
    convert(ann_dir, save_dir)

print('finish processing dataset...')

print('start checking dataset...')
images = glob.glob(os.path.join(save_path, 'images/*/*.jpg'))
anns = glob.glob(os.path.join(save_path, 'labels/*/*.txt'))

for img in images:
    ann = img.replace('images', 'labels').replace('.jpg', '.txt')
    if ann not in anns:
        print(img)
        os.unlink(img)

for ann in anns:
    img = ann.replace('labels', 'images').replace('.txt', '.jpg')
    if img not in images:
        print(ann)
        os.unlink(ann)
print('finish checking dataset...')