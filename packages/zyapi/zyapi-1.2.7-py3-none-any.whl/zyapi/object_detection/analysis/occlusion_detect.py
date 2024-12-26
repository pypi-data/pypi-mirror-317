import cv2
import numpy as np
import datetime
import copy
import warnings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
warnings.filterwarnings("ignore", category=RuntimeWarning)


def occlusion_detect(im, attr):
    boxes, scores, classes = list(), list(), list()
    dev_id = attr.get('dev_id')
    alarm_time = attr['dev_rules']['behavior_5000011']['alarm_time']
    refresh_time = attr['dev_rules']['behavior_5000011']['refresh_time']
    detect_interval = attr['dev_rules']['behavior_5000011']['detect_interval']
    detect_interval += alarm_time
    if dev_id not in attr.dev_rules['behavior_5000011'].get('occlusion'):
        attr.dev_rules['behavior_5000011']['occlusion'][dev_id] = Occlusion()
    try:
        res_count, restart_count = attr.dev_rules['behavior_5000011']['occlusion'][dev_id].occlusion_det(im, refresh_time, detect_interval)
    except Exception as e:
        attr.dev_rules['behavior_5000011']['occlusion'][dev_id] = Occlusion()
        logger.exception(f'occlusion detect error: {e}')
        return boxes, scores, classes

    if res_count >= 1 and restart_count == 0:
        classes.append('occlusion')
        scores.append(0.98)
        boxes.append([0, 0, 2, 2])

    return boxes, scores, classes


def get_corners(im):
    im = cv2.resize(im, (640, 480))
    im = im[int(480 / 8):int(480 / 8 * 7), 0:640]
    final_img = im
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(im, 400, 0.05, 10)
    corners = np.intp(corners)
    u = int(len(corners) ** 0.5)
    return u, im, final_img, corners


def get_pixel_matrix(im, pic_num_read, pixel_location, pixel_matrix, D, F, FC, FO, E, n):
    u, im, final_img, corners = get_corners(im)
    ground_img = copy.deepcopy(final_img)
    if pic_num_read == 0:
        if corners is not None:
            if u * u <= len(corners):
                num = 0
                for i in corners:
                    if num < u * u:
                        x, y = i.ravel()
                        pixel_location.append([int(y), int(x)])
                        a = im[y, x]
                        num = num + 1
                        pixel_matrix.append(a)
                        cv2.circle(final_img, (x, y), 3, 255, -1)

                    D = np.zeros((u, u))
                    F = np.zeros((u, u))
                    FC = np.zeros((u, u))
                    FO = np.zeros((u, u))
                    E = np.zeros((u, u))
                pixel_matrix = np.array(pixel_matrix).reshape((u, u))
                n = u

            else:
                for i in corners:
                    x, y = i.ravel()
                    pixel_location.append([int(y), int(x)])
                    a = im[y, x]
                    pixel_matrix.append(a)
                    cv2.circle(final_img, (x, y), 3, 255, -1)
                pixel_matrix = np.array(pixel_matrix).reshape((n, n))

    else:
        pixel_matrix = []
        for i in pixel_location:
            a = im[i[0], i[1]]
            pixel_matrix.append(a)
            cv2.circle(final_img, (i[1], i[0]), 3, 255, -1)
        pixel_matrix = np.array(pixel_matrix).reshape((n, n))
    return im, final_img, ground_img, pixel_location, pixel_matrix, D, F, FC, FO, E, n


def get_differential_image(im, count, d, f, D, F, FC, FO, E):
    a = 0.1
    E_max = 10
    TS = 30
    TF = 15
    l = 5
    count = count + 1

    if count <= 2:
        d.append(im)
    else:
        # 计算当前前景和原始前景
        FC = cv2.absdiff(im, d[-1])
        FC = cv2.threshold(FC, TS, 1, cv2.THRESH_BINARY)[1]
        FO = cv2.absdiff(im, d[0])
        FO = cv2.threshold(FO, TS, 1, cv2.THRESH_BINARY)[1]

    if count > 2:
        f.append(im)

    if len(f) > 1:
        # 计算差分图像
        F = cv2.absdiff(f[-1], f[0])
        F = cv2.threshold(F, TF, 1, cv2.THRESH_BINARY)[1]

        # 计算动态矩阵
        condition = (F == 0) & (D > 0)
        D[condition] = D[np.where(condition)] - 1
        condition = (F == 1)
        D[condition] = l

        # 3种情况分别更新背景
        condition = (FC == 1) & (FO == 1) & (D == 0)
        # d[0][condition] = d[-1][np.where(condition)]
        d[-1][condition] = im[np.where(condition)]
        condition = (FC == 1) & (FO == 0)
        d[-1][condition] = d[0][np.where(condition)]
        condition = (FC == 0) & (FO == 0) & (D == 0)
        d[-1][condition] = a * (im[np.where(condition)]) + (1 - a) * (d[-1][np.where(condition)])
        # d[0][condition] = a * (im[np.where(condition)]) + (1 - a) * (d[0][np.where(condition)])

        # 证据图像累加
        E[E == 255] = E_max
        condition = (FC == 0) & (FO == 1) & (D == 0)
        E[condition] = E[np.where(condition)] + 1
        condition = (FC == 1) | (FO == 0) | (D != 0)
        E[condition] = E[np.where(condition)] - 1
        condition = (E > E_max)
        E[condition] = E_max
        condition = (E < 0)
        E[condition] = 0
        E[E == E_max] = 255
        f.pop(0)
    return count, E, d, FC, FO, D


class Occlusion(object):
    def __init__(self):
        self.n = 15
        self.d_interval = 1
        self.u = 0
        self.occ = False
        self.restart_count = 0
        self.f, self.d, self.k, self.pic_num_read, self.pixel_location, self.pixel_matrix = self.init_parameter()
        self.D, self.F, self.FC, self.FO, self.E, self.count, self.pixel, self.constant_count = self.init_matrix(self.n)
        self.start_time = datetime.datetime.now()

    def init_parameter(self):
        f = []
        d = []
        k = 0
        pic_num_read = 0
        pixel_location = []
        pixel_matrix = []
        return f, d, k, pic_num_read, pixel_location, pixel_matrix

    def init_matrix(self, n):
        D = np.zeros((n, n))
        F = np.zeros((n, n))
        FC = np.zeros((n, n))
        FO = np.zeros((n, n))
        E = np.zeros((n, n))
        count = 0
        pixel = None
        constant_count = 0
        return D, F, FC, FO, E, count, pixel, constant_count

    def init_matrix_im(self, h, w):
        D = np.zeros((h, w))
        F = np.zeros((h, w))
        FC = np.zeros((h, w))
        FO = np.zeros((h, w))
        E = np.zeros((h, w))
        return D, F, FC, FO, E

    def occlusion_det(self, im, refresh_time, detect_interval):
        if self.pic_num_read == 0:
            self.u, _, _, _ = get_corners(im)
        if self.u > 8:
            im, final_img, ground_img, self.pixel_location, self.pixel_matrix, self.D, self.F, self.FC, self.FO, self.E, self.n = get_pixel_matrix(
                im, self.pic_num_read, self.pixel_location, self.pixel_matrix, self.D, self.F, self.FC, self.FO, self.E,
                self.n)
        else:
            im = cv2.resize(im, (640, 480))
            im = im[int(480 / 8):int(480 / 8 * 7), 0:640]
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            self.pixel_matrix = im
            h, w = im.shape
            if self.pic_num_read == self.d_interval:
                self.D, self.F, self.FC, self.FO, self.E = self.init_matrix_im(h, w)
                self.n = h

            # self.f, self.d, self.k, self.pic_num_read, self.pixel_location, self.pixel_matrix = self.init_parameter()
            # self.D, self.F, self.FC, self.FO, self.E, self.count, self.pixel, self.constant_count = self.init_matrix(
            #     self.n)
            # self.start_time = datetime.datetime.now()
            # return self.constant_count
        self.pic_num_read = self.pic_num_read + 1
        if self.pic_num_read - self.k == self.d_interval:
            self.k = self.pic_num_read
            self.count, self.E, self.d, self.FC, self.FO, self.D = get_differential_image(self.pixel_matrix, self.count,
                                                                                          self.d, self.f, self.D,
                                                                                          self.F, self.FC, self.FO,
                                                                                          self.E)
            final_frame = self.E
            final_frame = cv2.threshold(final_frame, 100, 255, cv2.THRESH_BINARY)[1]
            changed_pixel = np.sum(final_frame) / 255
            if (datetime.datetime.now() - self.start_time).seconds / 60 < refresh_time:
                if changed_pixel > 0.8 * (self.n * self.n):
                    self.constant_count += 1
                    if self.constant_count >= detect_interval:
                        self.occ = True
                else:
                    if self.occ:
                        self.restart_count += 1
                if self.restart_count >= detect_interval:
                    self.f, self.d, self.k, self.pic_num_read, self.pixel_location, self.pixel_matrix = self.init_parameter()
                    self.D, self.F, self.FC, self.FO, self.E, self.count, self.pixel, self.constant_count = self.init_matrix(
                        self.n)

                    self.occ = False
                    self.constant_count = 0
                    self.restart_count = 0
                    self.start_time = datetime.datetime.now()
            else:
                self.f, self.d, self.k, self.pic_num_read, self.pixel_location, self.pixel_matrix = self.init_parameter()
                self.D, self.F, self.FC, self.FO, self.E, self.count, self.pixel, self.constant_count = self.init_matrix(
                    self.n)

                self.occ = False
                self.constant_count = 0
                self.restart_count = 0
                self.start_time = datetime.datetime.now()

        return self.constant_count, self.restart_count
