import os
import cv2

"""
  标注文件，一个txt 中转换为VOC 的xml
  调整图片：为指定的宽,高，对应的标注文件也要改
"""
from xml.dom.minidom import Document
import pandas as pd


# resize images
def resize_imgs(rootdir, imgpath, savepath):
    df = pd.read_csv(rootdir + "/gt.txt", sep=";", names=list(["filename", "xmin", "ymin", "xmax", "ymax", "label"]))
    c = df["filename"].value_counts(ascending=True)
    for index, row in df.iterrows():
        img = cv2.imread(imgpath+row["filename"])
        new_img = cv2.resize(img, (416, 416))
        new_filename = row["filename"].split(".")[0]+".jpg"
        cv2.imwrite(savepath+new_filename, new_img)
        print(f"Conversion completed {index} picture.")


def writexml(filename, imgshape, bboxes, xmlpath , objectname):
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('images')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)

    filenamenode = doc.createElement('filename')
    filename_name = doc.createTextNode(filename)
    filenamenode.appendChild(filename_name)
    annotation.appendChild(filenamenode)

    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('GTSDB Database'))
    source.appendChild(database)

    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(imgshape[0])))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(imgshape[1])))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(imgshape[2])))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)

    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segmented)

    for i in range(len(bboxes)):
        bbox = bboxes[i]
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode(objectname[i]))
        objects.appendChild(object_name)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('unspecified'))
        objects.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('0'))
        objects.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode("unknow"))
        objects.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        objects.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmin.appendChild(doc.createTextNode(str(bbox[0])))
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin.appendChild(doc.createTextNode(str(bbox[1])))
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax.appendChild(doc.createTextNode(str(bbox[2])))
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax.appendChild(doc.createTextNode(str(bbox[3])))
        bndbox.appendChild(ymax)
    f = open(xmlpath, "w")
    f.write(doc.toprettyxml(indent=''))
    f.close()




def txt_xml(rootdir):
    df = pd.read_csv(rootdir + "/gt.txt", sep=";", names=list(["filename", "xmin", "ymin", "xmax", "ymax", "label"]))
    c = df["filename"].value_counts(ascending=True)
    bboxes = []
    objectname = []
    saveimg = [416, 416, 3]
    w = 1360/416
    h = 800/416
    classes = []
    with open(rootdir+"/GTSDB.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    print(classes)
    with open(rootdir + "/gt.txt", 'r') as gtfiles:
        while(True):
            info1 = gtfiles.readline().split(";")
            filename = info1[0]
            if filename == "":
                break
            bbox = (int(int(str.strip(info1[1])) / w), int(int(str.strip(info1[2])) / h), int(int(str.strip(info1[3]))/w), int(int(str.strip(info1[4])) /h))
            bboxes.append(bbox)
            label = str(classes[int(info1[5])])
            objectname.append(label)
            numbbox = c[filename]
            if numbbox != 1:
                for i in range(numbbox-1):
                    info1 = gtfiles.readline().split(";")
                    bbox = (int(int(str.strip(info1[1])) / w), int(int(str.strip(info1[2])) / h),
                            int(int(str.strip(info1[3])) / w), int(int(str.strip(info1[4])) / h))
                    bboxes.append(bbox)
                    label = str(classes[int(info1[5])])
                    objectname.append(label)

            xmlpath = rootdir + "\\Annotations\\" + filename.split(".")[0] + ".xml"
            writexml(filename.split(".")[0], saveimg, bboxes, xmlpath, objectname)
            with open(rootdir+"\\ImageSets\\Main\\train.txt", 'a') as f:
                f.write(filename.split(".")[0]+"\n")
            bboxes = []
            objectname = []


if __name__ == '__main__':

    rootdir = os.getcwd()
    # resize_images
    org_images_path = rootdir+"\\FullIJCNN2013\\"
    save_images_path = rootdir+"\\VOC2007\\JPEGimages\\"
    # resize_imgs(rootdir, org_images_path, save_images_path)

    # covert 1txt_to_xml(voc)
    rootdir = rootdir+"\\VOC2007\\"
    txt_xml(rootdir)  # generation xml files






