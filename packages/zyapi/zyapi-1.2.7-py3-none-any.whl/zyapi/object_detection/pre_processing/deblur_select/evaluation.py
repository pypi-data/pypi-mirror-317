# coding:utf-8
# author @qianlinrui

import cv2
import numpy as np
from skimage import filters


class Evaluate(object):
    def __init__(self, img):
        self.img = img

    def cal_smd2(self):
        '''计算灰度方差乘'''
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        w = shape[0]
        h = shape[1]
        # TODO: 如果len(shape) != 3的情况下，以下代码会出错，这里应该增加相应的处理
        mat = np.abs(grayimg[0:w - 1, 0:h - 1] - grayimg[1:w, 0:h - 1]) * np.abs(
            grayimg[0:w - 1, 0:h - 1] - grayimg[:][0:w - 1, 1:h])
        SMD2 = np.sum(np.sum(mat, axis=0), axis=0)
        return SMD2

    def cal_smd(self):
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        w = shape[0]
        h = shape[1]
        mat = np.abs(grayimg[:][1-h]-grayimg[:][0:h-1]) + np.abs(grayimg[0:w-1] - grayimg[1:w])
        SMD = np.sum(np.sum(mat, axis=0), axis=0)
        return SMD

    def cal_brenner_gradient(self):
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        w = shape[0]
        mat = np.abs(grayimg[2:w]-grayimg[0:w-2])
        BG1 = np.sum(np.sum(mat, axis=0),axis=0)
        return BG1

    def cal_variance(self):
        '''方差函数'''
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        variance = np.var(grayimg)
        return variance

    def cal_energy_gradient(self):
        '''计算能量梯度'''
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        w = shape[0]
        h = shape[1]
        mat1 = (grayimg[1:w]-grayimg[0:w-1]) * (grayimg[1:w]-grayimg[0:w-1])
        mat2 = (grayimg[:][1:h]-grayimg[:][0:h-1]) * (grayimg[:][1:h]-grayimg[:][0:h-1])
        EG1 = np.sum(np.sum(mat1, axis=0), axis=0) + np.sum(np.sum(mat2, axis=0), axis=0)
        return EG1

    def cal_tenen_gradient(self):
        ''' 计算Tenengrad 梯度'''
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        gx = np.multiply(filters.sobel_h(grayimg), filters.sobel_h(grayimg))
        gy = np.multiply(filters.sobel_v(grayimg), filters.sobel_v(grayimg))
        TG = np.sum(np.sum(np.sqrt(gx + gy), axis=0), axis=0)
        return TG

    def cal_laplacian_gradient(self):
        img = self.img
        shape = img.shape
        if len(shape) == 3:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            grayimg = grayimg.astype(np.int16)
        else:
            grayimg = self.img.astype(np.int16)
        g = np.abs(filters.laplace(grayimg))
        LG = np.sum(np.sum(g, axis=0), axis=0)
        return LG
