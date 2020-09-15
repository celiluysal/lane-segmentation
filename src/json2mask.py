import numpy as np
import time
import json
import cv2
import re
import os
from os import listdir
from os.path import isfile, join


JSON_DIR = "../data/jsons"
MASK_DIR = "../data/masks"

lanes_mask_list = []
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)

def clean_TypeName(_name):
    pattern = r"\.[0-9a-z].*"
    name = re.sub(pattern, '', _name)
    return name

class ColoredPoints(object):
    color = (0,0,0)
    def __init__(self, points, line_type):
        self.points = []
        self.points.append(points)
        if (line_type == "Solid Line"):
            self.color = red
        elif (line_type == "Dashed Line"):
            self.color = green



class LaneMask(object):
    def __init__(self, width, height, rgb_points:ColoredPoints, name):
        self.width = width
        self.height = height
        self.rgb_points = rgb_points
        self.name = clean_TypeName(name)

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

        line_count = 0
        obj_points_list = []

        for obj in json_objs:
            if obj["classTitle"] == "Solid Line":
                line_count += 1
                points = obj["points"]["exterior"]
                solid_rgb_points = ColoredPoints(points, "Solid Line")
                obj_points_list.append(solid_rgb_points)

            elif obj["classTitle"] == "Dashed Line":
                line_count += 1
                points = obj["points"]["exterior"]
                dashed_rgb_points = ColoredPoints(points, "Dashed Line")
                obj_points_list.append(dashed_rgb_points)

        if (line_count > 0):
            lanes = LaneMask(width, height, obj_points_list, file_name)
            lanes_mask_list.append(lanes)
        else:
            empty_rgb_points = ColoredPoints([], "No Line")
            obj_points_list = empty_rgb_points
            lanes = LaneMask(width, height, obj_points_list, file_name)
            lanes_mask_list.append(lanes)

def draw_and_save_line(_LaneMask:LaneMask):
    mask = np.zeros((_LaneMask.height, _LaneMask.width, 3), np.uint8)
    rgb_points_list = _LaneMask.rgb_points
    isClosed = False
    thickness = 2

    for rgb_points in rgb_points_list:
        color = rgb_points.color
        pts = np.array(rgb_points.points, np.int32)
        pts = pts.reshape((-1,1,2))
        image = cv2.polylines(mask, [pts], isClosed, color, thickness) 

    cv2.imwrite(join(MASK_DIR,_LaneMask.name + "_mask.png"),image)
        


if __name__ == '__main__':
    start = time.time()
    read_jsons()
    end = time.time()
    print("read jsons: ", (end - start) / 60)
        
    start = time.time()
    for mask in lanes_mask_list:
        draw_and_save_line(mask)
    end = time.time()
    print("masks: ", (end - start) / 60)


