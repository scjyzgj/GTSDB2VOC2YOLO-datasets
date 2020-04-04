import xml.etree.ElementTree as ET
import os



'''
 在VOC2007 下的labels 文件夹下创建了对应的每一张图片对应的同名txt文件
 在项目的根目标下，创建了2007_train.txt,2007_val.txt,2007_test.txt,
'''

# sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
sets = [('2007', 'train')]
classes = []
with open(os.getcwd()+"\\GTSDB.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x, y, w, h


def convert_annotation(year, image_id,wd):
    in_file = open(wd+'/VOC%s/Annotations/%s.xml' % (year, image_id))
    out_file = open(wd+'/VOC%s/labels/%s.txt' % (year, image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = os.getcwd()
for year, image_set in sets:
    if not os.path.exists(wd+'/VOC%s/labels/'%(year)):
        os.makedirs(wd+'/VOC%s/labels/'%(year))
    image_ids = open(wd+'/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open(wd+'%s_%s.txt' % (year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOC%s/JPEGImages/%s.jpg\n' % (wd, year, image_id))
        convert_annotation(year, image_id, wd)
    list_file.close()

