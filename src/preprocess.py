import numpy as np
import time
import json
import cv2
import re
import os
from os import listdir
from os.path import isfile, join

import torch
import glob

IMG_DIR = "../data/images"
MASK_DIR = "../data/masks"

def tensorize_image(image_path, output_shape):
    batch_images = []
    for file_name in image_path:
        img = cv2.imread(file_name, cv2.IMREAD_COLOR)
        img = cv2.resize(img,output_shape)
        batch_images.append(img)

    batch_images = np.array(batch_images)
    # torch_image = torch.from_numpy(batch_images)
    # image_tensor = torch_image.cuda()
    # return image_tensor 
    return batch_images 
    #[4765, 20, 20, 3] [B,W,H,C]

def tensorize_mask(mask_path, output_shape ,n_class):
    batch_masks = list()
    for file_name in mask_path:
        mask = cv2.imread(file_name, cv2.IMREAD_COLOR)
        mask = cv2.resize(mask, output_shape)
        mask = mask / 255
        # print("mask", mask)
        mask = one_hot_encode(mask, n_class)
        # print("mask enc", mask)
        batch_masks.append(mask)
  
    batch_masks = np.array(batch_masks)
    # print("mask enc batch", batch_masks)
    torch_mask = torch.from_numpy(batch_masks)
    # print("mask torch", torch_mask)
    mask_tensor = torch_mask.cuda()
    # print("mask tens", mask_tensor)
    # print("mask tens len", len(mask_tensor))
    #[4765, 20, 20, 2] [B,W,H,C] 
    return mask_tensor

def one_hot_encode(data, n_class):
    encoded_data = np.zeros((*data.shape, n_class), dtype=np.int) # (width, height, number_of_class)'lık bir array tanımlıyorum.    print(data)
    print("1",encoded_data.shape)
    for lbl in range(n_class):
        encoded_labels = [0] * n_class # buraya da [0, 0, .., 0] (n tane 0) bir encoded_labels, bizim durumumuz için [0, 0, 0] oluyor bu (n=3)
        encoded_labels[lbl] = 1 # lbl = 0 için (arkaplan)    [1, 0, 0] labelini oluşturuyorum, 
                                # lbl = 1 için (solid line)  [0, 1, 0] labelini oluşturuyorum.
                                # lbl = 2 için (dashed line) [0, 0, 1] labelini oluşturuyorum.
        print()
        print(encoded_labels)

        numerical_class_inds = np.empty(data.shape, dtype=bool)
        print(type(numerical_class_inds))
        print("nm", numerical_class_inds.shape)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    if (lbl == 0):
                        numerical_class_inds[i][j][k] = data[i][j][k] == 0
                    elif (lbl == 1):
                        numerical_class_inds[i][j][k] = data[i][j][k] == 1 and k == 1
                    elif (lbl == 2):
                        numerical_class_inds[i][j][k] = data[i][j][k] == 1 and k == 2

        # print(numerical_class_inds)
        print("4",encoded_data.shape)
        encoded_data[numerical_class_inds] = encoded_labels # lbl = 0 için tüm F'in sahip olduğu tüm w,h ikililerini [1, 0]'a eşitliyorum.
                                                            # lbl = 1 için tüm O'un sahip olduğu tüm w,h ikililerini [0, 1]'e eşitliyorum.
        print("5",encoded_data.shape)
    # print(encoded_data)
    return encoded_data

if __name__ == '__main__':
    
    # image_file_names = glob.glob(IMG_DIR + "/*")
    # image_file_names.sort()
    # batch_image_list = image_file_names[:5] #first n
    # batch_image_tensor = tensorize_image(batch_image_list, (20,20))
    
    # print(batch_image_list)
    # print(batch_image_tensor.dtype)
    # print(type(batch_image_tensor))
    # print(batch_image_tensor.shape)

    # print("------------")    
    
    mask_file_names = glob.glob(MASK_DIR + "/*")
    mask_file_names.sort()
    batch_mask_list = mask_file_names[:1] #first n
    batch_mask_tensor = tensorize_mask(batch_mask_list, (5,5), 3)
    
    print(batch_mask_list)
    print(batch_mask_tensor.dtype)
    print(type(batch_mask_tensor))
    print(batch_mask_tensor.shape)  