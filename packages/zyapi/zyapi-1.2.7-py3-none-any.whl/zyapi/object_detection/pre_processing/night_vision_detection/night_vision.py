import cv2
import numpy as np
import time
import os
from ...utils.parametar import HYPER_PARA


class NightVisionDetection():
    """根据HSV中H（色度）判断图片是否是夜视状态"""
    def __init__(self):
        self.runtime = 0
        self.result = 0

    def get_chroma(self, in_img):
        """
        description: 转换为HSV，根据色度H和明度V判断是否是夜视

        param:
            in_img:  ndarray图片数组
        return:
            flag： True or False
        """
        start = time.time()

        in_img = cv2.resize(in_img, (1000, 1000))
        hsv = cv2.cvtColor(in_img, cv2.COLOR_BGR2HSV)
        channels = cv2.split(hsv)
        h, w = in_img.shape[0], in_img.shape[1]

        h_channel = channels[0]
        v_channel = channels[2]
        total_h = np.sum(h_channel)
        total_v = np.sum(v_channel)
        avg_h = total_h / (h*w)
        avg_v = total_v / (h*w)

        self.runtime = time.time() - start
        self.result = [avg_h, avg_v]
        if avg_h < 10 or avg_v < 25:
            return True
        else:
            return False


if __name__ == "__main__":
    night_vision_detection = NightVisionDetection()

    img_path = os.path.join(HYPER_PARA.project_dir, HYPER_PARA.test_img_dir, 'night_vision_detection')
    images = os.listdir(img_path)
    for image in images:
        if image.endswith('jpg'):
            img = cv2.imread(os.path.join(img_path, image))
            flag = night_vision_detection.get_chroma(img)

            cv2.putText(img, "time is :{}".format(night_vision_detection.runtime), (100, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (105, 255, 0), 2)
            cv2.putText(img, "image avg_h:{}".format(night_vision_detection.result[0]), (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (105, 255, 0), 2)
            cv2.putText(img, "image avg_v:{}".format(night_vision_detection.result[1]), (100, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (105, 255, 0), 2)
            cv2.putText(img, "Is it night vision mode:{}".format(flag), (100, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (105, 255, 0), 2)
            cv2.namedWindow('img', 0)
            cv2.resizeWindow('img', 1000, 1000)
            cv2.imshow("img", img)
            key = cv2.waitKey(0)

