import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob

classes =["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]

#change size to yolo data
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y= (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    y = y*dh
    w = w*dw
    h = h*dh
    return (x,y,w,h)

#get information from xml
def conver_annotation(image_name):
    in_file = open('./ANNOTATIONS/' + image_name[:-3] + 'xml')
    out_file = open('./LABELS/' + image_name[:-3] + 'txt','w')
    tree = ET.parse(in_file)
    root = tree.getroot
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('obeject'):
        cls = obj.find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.fin('xmax').text),float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

if __name__ =='__main__':
    for image_path in glob.glob("./IMAGES/*.jpg"):
        image_name = image_path.split('\\')[-1]
        print(image_path)
        conver_annotation(image_name)
