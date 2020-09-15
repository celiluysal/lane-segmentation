import cv2 
import numpy as np 
  
# path 

  
# Reading an image in default 
# mode 
mask = np.zeros((1208, 1920, 3), np.uint8)
  
# Window name in which image is 
# displayed 
window_name = 'Image'
  
# Polygon corner points coordinates 
pts1 = np.array([[]], np.int32)
pts2 = np.array([
                    [
                        1229,
                        613
                    ],
                    [
                        1235,
                        601
                    ]
                ], np.int32)
pts3 = np.array([
                    [
                        1061,
                        622
                    ],
                    [
                        1129,
                        605
                    ]
                ], np.int32)
pts4 = np.array([
                    [
                        0,
                        866
                    ],
                    [
                        156,
                        822
                    ],
                    [
                        299,
                        782
                    ],
                    [
                        468,
                        734
                    ],
                    [
                        651,
                        685
                    ],
                    [
                        775,
                        655
                    ],
                    [
                        860,
                        636
                    ],
                    [
                        944,
                        621
                    ],
                    [
                        1014,
                        610
                    ]
                ], np.int32)
pts5 = np.array([
                    [
                        1919,
                        799
                    ],
                    [
                        1680,
                        740
                    ],
                    [
                        1621,
                        723
                    ],
                    [
                        1505,
                        691
                    ],
                    [
                        1355,
                        636
                    ],
                    [
                        1337,
                        624
                    ],
                    [
                        1328,
                        613
                    ],
                    [
                        1323,
                        602
                    ],
                    [
                        1314,
                        588
                    ],
                    [
                        1304,
                        579
                    ],
                    [
                        1288,
                        575
                    ]
                ], np.int32)



points = []
points.append(pts1)
points.append(pts2)
points.append(pts3)
points.append(pts4)
points.append(pts5)


  
isClosed = False    
  
# Blue color in BGR 
blue = (255, 0, 0) 
red = (0,0,255)
  
# Line thickness of 2 px 
thickness = 2
  
# Using cv2.polylines() method 
# Draw a Blue polygon with  
# thickness of 1 px 


for i in points:
    pts = np.array(i, np.int32)
    pts = pts.reshape((-1, 1, 2)) 
    mask = cv2.polylines(mask, [pts], isClosed, blue, thickness) 

  
# Displaying the image 
cv2.imshow('image', mask) 
cv2.waitKey(0)
cv2.destroyAllWindows() 