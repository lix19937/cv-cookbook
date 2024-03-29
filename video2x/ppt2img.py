
# ppt 转换为图片   

import cv2
import numpy as np
import os
import sys

def average_hash(img):
    ihash = img > np.mean(img)
    return ihash

def calc_diff(prev, curr, w=50, h=50):
    try:
        prev = cv2.resize(prev, (w,h))
        curr = cv2.resize(curr, (w,h))
        hash_prev = prev > np.mean(prev)
        hash_curr = curr > np.mean(curr)
        diff = hash_prev & hash_curr
        return np.sum(diff)
    except:
        return 0

def proc(fname):
    os.mkdir(fname.split(".")[0])
    
    diff = []
    frames = []
    cap = cv2.VideoCapture(fname)
    
    f = 0
    prev = None
    prev_diff = 1000
    prev_frame = -1000
    
    while cap.isOpened():
        f += 1
        print("frame: %d" %f)

        ret, frame = cap.read()
        if not ret:
          break
        curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        curr_diff = calc_diff(prev, curr)
        diff.append(curr_diff)
        if abs(curr_diff - prev_diff) > 50 and f - prev_frame > 10:
            frames.append(frame)
            ff = fname.split(".")[0]
            file = "%s/%d.jpg"%(ff, len(frames))
            print("frame file: %s"%file)
            cv2.imwrite(file, frame)
            prev_frame = f
        prev = curr
        prev_diff = curr_diff
    print("Task: %s finished"%(fname.split(".")[0]))
    return frames

proc(sys.argv[1])

## python ppt2img.py input/DriveWorks_Image_Module_Samples_.mp4

