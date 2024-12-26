# coding: utf-8
# author @qianlinrui
import json
import numpy as np 
import os 
import cv2
import glob
import time
import sys 
import logging
import random
from itertools import chain

from ...utils.parametar import HYPER_PARA
from .evaluation import Evaluate


def save_json_file(obj, output_file):
    if output_file is not None:
        if not os.path.isdir(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        with open(output_file, 'w') as f:
            json.dump(obj, f)


def read_json_file(input_file):
    obj = None
    if os.path.getsize(input_file) > 0:
        try:
            with open(input_file, 'r') as f:
                # obj = pickle.load(f)
                obj = json.load(f)
                # logging.info(msg="In load_object() -> success...")
        except EOFError as e:
            logging.error("In load_object() -> input_file: {0}, error: {1}, obj: {2}".format(input_file, e, obj))
    else:
        logging.error("In load_object() -> input_file: {0}, error: size is 0, obj: {1}".format(input_file, obj))
    return obj


class ImageClassAI(object):
    def __init__(self, image_path=None, best_smd2=0, best_laplace=0):
        self.image_path = image_path
        self.best_smd2 = best_smd2
        self.best_laplace = best_laplace


# image rotation
def rotate(image, angle):
    (h, w) = image.shape[0:2]

    center = (w/2, h/2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))

    return rotated


class DeblurSelect(object):
    def __init__(self):
        self.estimator = None  # 姿态估计模型
        self.train_data_list = dict()  # 保存训练样本的路径以及smd2
        self.best_one_dict = dict()  # 挑选出最清晰的图片路径
        self.train_data_info = dict()  # 保存挑选出的训练样本的路径
        self.add_image = list()  # 传入一个person_list_id时增加到训练样本里的图片列表
        self.delete_image = list()  # 传入一个person_list_id时从训练样本里删除的图片列表
        self.thread = HYPER_PARA.sharpness_threshold  # 峰值信噪比、结构相似性阈值、smd2阈值、Laplace阈值
        self.anti_size = 112  # 活体检测时，输入图片的尺寸

    @classmethod
    def is_blur(self, image):
        # 评价单张图像质量
        # crop_image = image[21:159, 21:159, :]
        w, h, _ = image.shape
        # crop_image = image[int(0.5 * w) - 69:int(0.5 * w) + 69, int(0.5 * h) - 69:int(0.5 * h) + 69, :]
        # rgb_crop_image = crop_image[..., ::-1]
        # evaluate = Evaluate(rgb_crop_image)
        evaluate = Evaluate(image)
        smd2 = evaluate.cal_smd2()
        laplace = evaluate.cal_laplacian_gradient()
        # 阈值判断，保证训练集和挑选出的图片尽量清晰
        # print(smd2, laplace, HYPER_PARA.sharpness_threshold[2], HYPER_PARA.sharpness_threshold[3])
        if (smd2 < HYPER_PARA.sharpness_threshold[2]) or (laplace < HYPER_PARA.sharpness_threshold[3]):
            return True, smd2, laplace
        return False, smd2, laplace

    def better_clear(self, image1, image2):
        """
        通过smd2和laplace比较两张图片哪张更清晰
        :param image1: CompareImage的实例化
        :param image2: CompareImage的实例化
        :return: 最清晰的一个对象,true is image1,false is image2
        """

        _, image1_best_smd2, image1_best_laplace = self.is_blur(image1)
        _, image2_best_smd2, image2_best_laplace = self.is_blur(image2)

        if image1_best_smd2 > image2_best_smd2 and image1_best_laplace > image2_best_laplace:  
            return image1,True

        elif image1_best_smd2 < image2_best_smd2 and image1_best_laplace < image2_best_laplace: 
            return image2,False

        elif image1_best_smd2 > image2_best_smd2 and image1_best_laplace < image2_best_laplace:
            condition_left = (image1_best_smd2 - image2_best_smd2) / (image1_best_smd2 + image2_best_smd2)
            condition_right = abs(image1_best_laplace - image2_best_laplace) / (image1_best_smd2 + image2_best_laplace)

            return image1,True if condition_left > condition_right else image2, False

        else:
            condition_left = abs(image1_best_smd2 - image2_best_smd2) / (image1_best_smd2 + image2_best_smd2)
            condition_right = (image1_best_laplace - image2_best_laplace) / (image1_best_laplace + image2_best_laplace)

            return image2,False if condition_left > condition_right else image1,True

    def blur_sort(self, smd2_laplace, blur_type='smd2'):
        """
        根据smd2或者laplace进行排序
        :param smd2_laplace:
        :param blur_type:
        :return:
        """
        if blur_type =='smd2':
            sort_list = smd2_laplace[:, 0]
        if blur_type == 'laplace':
            sort_list = smd2_laplace[:, 1]
        if blur_type == 'mix':
            sort_list = smd2_laplace[:, 2]
        sort_index = np.argsort(-sort_list)
        return sort_index

    def image_blur_sort(self, root_path, images_path, recommend_num = 10 , sort_type = 'laplace'):
        """
        对图片进行排序
        :param images_path:图片路径组成的列表
        :return:
        """
        image_list = []
        try:
            if type(images_path) is str:
                if os.path.isdir(images_path):
                    image_list = glob.glob(images_path + '/*' + HYPER_PARA.picture_format)
            elif type(images_path) is list:
                image_list = images_path
            else:
                logging.error(msg="input type is not path or list")
        except Exception as e:
            raise TypeError('Input type error!')

        if len(image_list) <= recommend_num:
            #image numbers is less than selected number
            return images_path
        else:
            
            smd2_laplace = []  # smd2, laplace
            # angles_list = []  # yaw_angle, roll_angle, pitch_angle,

            for image_path in image_list:
                start_time = time.time()
                json_file_path = os.path.join(root_path,(image_path.split('/')[-1]).split('.')[0]+'.json')
    
                if os.path.exists(json_file_path):
                    print(f"{json_file_path} file alreay exists")
                    image_message = read_json_file(json_file_path)
                    if 'laplace' is image_message.keys():
                        laplace = image_message['laplace']
                    else:
                        image = cv2.imread(image_path)
                        # w, h, _ = image.shape
                        # crop_image = image[int(0.5 * w) - 69:int(0.5 * w) + 69, int(0.5 * h) - 69:int(0.5 * h) + 69, :]
                        # rgb_crop_image = crop_image[..., ::-1]
                        # evaluate = Evaluate(rgb_crop_image)
                        # laplace = evaluate.cal_laplacian_gradient()
                        _, _, laplace = self.is_blur(image)
                        
                    smd2 = image_message['smd2']['smd2']
                    # yaw_angle = image_message['angles']['yaw']
                    # roll_angle = image_message['angles']['roll']
                    # pitch_angle = image_message['angles']['pitch']
                    mix_blur = smd2 + laplace
                    smd2_laplace.append([smd2, laplace, mix_blur])
                    # angles_list.append([yaw_angle, roll_angle, pitch_angle])
                else:
                    image = cv2.imread(image_path)
                    is_blur_bool, smd2, laplace = self.is_blur(image)
                    mix_blur = smd2 + laplace
                    is_hog_front = True
                    message_dict = dict()
                    message_dict['laplace'] = {'laplace': float(laplace)}
                    message_dict['smd2'] = {'smd2': int(smd2), 'isblur': '1' if is_blur_bool else '0'}
                    message_dict['mix'] = {'mix':float(mix_blur)}
                    message_dict['hog'] = '1' if is_hog_front else '0'
                    filter_message_file = json_file_path
                    save_json_file(message_dict, filter_message_file)
                    # yaw_angle = angles[1]
                    # roll_angle = angles[0]
                    # pitch_angle = angles[2]
                    smd2_laplace.append([smd2, laplace,mix_blur])
                    # angles_list.append([yaw_angle, roll_angle, pitch_angle])
                    print(time.time()-start_time)

            # 分别按照每个指标对数据进行排序
            # yaw_index = self.angle_sort(angles, angle_type='yaw')
            # roll_index = self.angle_sort(angles, angle_type='roll')
            # pitch_index = self.angle_sort(angles, angle_type='pitch')
            smd2_laplace = np.array(smd2_laplace)
            # angles = np.array(angles_list)
            smd2_index = self.blur_sort(smd2_laplace, blur_type='smd2')
            laplace_index = self.blur_sort(smd2_laplace, blur_type='laplace').tolist()
            mix_index = self.blur_sort(smd2_laplace, blur_type='mix').tolist()
            mess_dict =[]
            
            if sort_type == 'smd2_index':
                for i in range(len(image_list)):
                    mess_dict.append(image_list[smd2_index[i]])
            elif sort_type == 'laplace_index':
               for i in range(len(image_list)):
                    mess_dict.append(image_list[laplace_index[i]])
            elif sort_type == 'mix_index':   
                for i in range(len(image_list)):
                    print(i,mix_index[i],image_list[13])
                    mess_dict.append(image_list[mix_index[i]])

            return mess_dict

        # 初始添加20个样本
        #     mess_index = []
        #     init_num = int(recommend_num / 5)
            
        #     # mess_index.append(yaw_index[0:init_num])
        #     # mess_index.append(roll_index[0:init_num])
        #     # mess_index.append(pitch_index[0:init_num])
        #     mess_index.append(smd2_index[0:init_num])
        #     mess_index.append(laplace_index[0:init_num])
        #     mess_index = list(chain.from_iterable(mess_index))
        #     mess_index = list(set(mess_index))  # 去重操作
        #     i = init_num
        #     # 继续添加样本直到样本数大于20个
        #     while len(mess_index) <= recommend_num:
        #         # mess_index.append(yaw_index[i])
        #         # mess_index.append(roll_index[i])
        #         # mess_index.append(pitch_index[i])
        #         mess_index.append(smd2_index[i])
        #         mess_index.append(laplace_index[i])
        #         mess_index = list(set(mess_index))
        #         i += 1
        #     print(mess_index)
        # # 打乱顺序，返回20个图片
        # random.shuffle(mess_index)
        # return [images_path[i] for i in mess_index[0:recommend_num]]


if __name__ == '__main__':
    
    data_path = '/home/amax/5.gitee/zt-video-analysis-system/mlc_computing_core/data/0ef9d8a9-d7ba-5dc0-8873-504cd48a6933'
    images_path = glob.glob(data_path + '/*.jpg')
    ds = DeblurSelect()

    # demo1: 从一组图片绝对地址列表中，挑选最清晰的那张，TODO :返回最清晰图的绝对路径
    image_one = cv2.imread(os.path.join(data_path,'test_1.jpg'))
    image_two = cv2.imread(os.path.join(data_path,'test_6.jpg'))
    print(image_two.shape)

    start = time.time()
    image_better_result = ds.better_clear(image_one,image_two)
    end = time.time()
    
    print(end-start,image_better_result[1])
  
    # demo2: 排序得到推荐的12张图片
    print(images_path)
    images = [cv2.imread(im) for im in images_path]
    start = time.time()
    recommend_images = ds.image_blur_sort(data_path, images_path, recommend_num=10, sort_type= 'mix_index')
    print(recommend_images)
    end = time.time()
    
    print('sort time is {}'.format((end - start) / len(images_path)))
