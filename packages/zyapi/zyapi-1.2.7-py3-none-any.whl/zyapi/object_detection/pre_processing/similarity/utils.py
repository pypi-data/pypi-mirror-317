import cv2
import numpy as np


def phash(img):
    img = cv2.resize(img, (50, 50))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(np.float32)
    img = cv2.dct(img)
    img = img[0:10, 0:10]
    im_list = img.flatten().tolist()
    avg = sum(im_list) * 1 / len(im_list)
    avg_list = ['0' if i < avg else '1' for i in im_list]
    return ''.join(['%x' % int(''.join(avg_list[x:x+4]), 2) for x in range(0, 100, 1)])


def distance(hash1, hash2):
    count = 0
    assert len(hash1) == len(hash2)
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            count += 1
    return count
