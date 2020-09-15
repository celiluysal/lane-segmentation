import numpy as np
import time
import json
import cv2
import re
import os
from os import listdir
from os.path import isfile, join

solidline_mask_list = []
dashedline_mask_list = []

JSON_DIR = "../data/jsons"
solid_line_masks_DIR = "../data/masks/solid_line_masks"
dashed_line_masks_DIR = "../data/masks/dashed_line_masks"

def clean_TypeName(_name):
    pattern = r"\.[0-9a-z].*"
    name = re.sub(pattern, '', _name)
    return name

class LaneMask(object):
    def __init__(self, width, height, points, name, line_type):
        self.width = width
        self.height = height
        self.points = []
        self.points.append(points)
        self.name = clean_TypeName(name)
        self.line_type = line_type

def read_jsons():
    json_file_names = [f for f in listdir(JSON_DIR) if isfile(join(JSON_DIR, f))]
    json_file_names.sort()
    for file_name in json_file_names:
        json_path = os.path.join(JSON_DIR, file_name)
        json_file = open(json_path, "r")
        json_dict = json.load(json_file)
        width = json_dict["size"]["width"]
        height = json_dict["size"]["height"]
        json_objs = json_dict["objects"]

        solid_line_count = 0
        dashed_line_count = 0

        for obj in json_objs:
            if obj["classTitle"] == "Solid Line":
                solid_line_count += 1
                points = obj["points"]["exterior"]
                if (solid_line_count > 1):
                    solid_line.points.append(points)
                else:
                    solid_line = LaneMask(width, height, points, file_name, "solid")
            elif obj["classTitle"] == "Dashed Line":
                dashed_line_count += 1
                points = obj["points"]["exterior"]
                if (dashed_line_count > 1):
                    dashed_line.points.append(points)
                else:
                    dashed_line = LaneMask(width, height, points, file_name, "dashed")

        if (solid_line_count == 0):
            solid_line = LaneMask(width, height, [], file_name, "solid")
        if (dashed_line_count == 0):
            dashed_line = LaneMask(width, height, [], file_name, "dashed")

        solidline_mask_list.append(solid_line)
        dashedline_mask_list.append(dashed_line)

def draw_and_save_line(_LaneMask:LaneMask):
    mask = np.zeros((_LaneMask.height, _LaneMask.width, 3), np.uint8)
    points_list = _LaneMask.points
    isClosed = False
    color = (255, 255, 255) #white
    thickness = 2

    for points in points_list:
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1,1,2))
        image = cv2.polylines(mask, [pts], isClosed, color, thickness) 

    if(_LaneMask.line_type == "solid"):
        cv2.imwrite(join(solid_line_masks_DIR,_LaneMask.name + "_solid_mask.png"),image)
    elif (_LaneMask.line_type == "dashed"):
        cv2.imwrite(join(dashed_line_masks_DIR, _LaneMask.name + "_dashed_mask.png"),image)


if __name__ == '__main__':
    start = time.time()
    read_jsons()
    end = time.time()
    print("read jsons: ", (end - start) / 60)
        
    start = time.time()
    for solid_mask in solidline_mask_list:
        draw_and_save_line(solid_mask)
    end = time.time()
    print("draw solid masks: ", (end - start) / 60)

    start = time.time()
    for dashed_mask in dashedline_mask_list:
        draw_and_save_line(dashed_mask)
    end = time.time()
    print("draw dashed masks: ", (end - start) / 60)
