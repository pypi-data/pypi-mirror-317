# coding: utf-8
import os
import cv2
import contextlib
import threading

from queue import Queue
from visface.main import VisFace
from ..utils.logger import setup_logger
from ..utils.parametar import HYPER_PARA
from ..utils.base_utils import alarm_statistics
from ..utils.workspace import AttrDict, load_config, create
from ..pre_processing.deblur_select.select_image import DeblurSelect
from ..pre_processing.similarity.main import Similarity
from ..pre_processing.night_vision_detection.night_vision import NightVisionDetection
from ..post_processing.postprocess import ImageProcess
from ..post_processing.recognition_mode.main import RecognitionMode


logger = setup_logger(__name__)
fire = {}


class BaseObjectDetect:
    lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.attr = None
        self.track = None
        self.detect = None
        self.recognition_mode = None
        self.similarity = Similarity()

        self.test = kwargs.get('test', True)
        self.cuda = kwargs.get('cuda', False)
        self.cache = kwargs.get('cache', '/home/sweet/.mx/')
        self.activate = kwargs.get('activate', False)
        self.face_handle = VisFace(cuda=self.cuda, cache=self.cache)

        self.warmup()
        self.dev_id = {}
        self.rules_dict = AttrDict()

        self.result_queue = Queue()
        self.post_processing_thread = None

    def warmup(self):
        # logger.info('warmup face detection...')
        addr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'liu.jpg')
        im = cv2.imread(addr)
        self.face_handle.register(im, 'test')
        self.face_handle.delete('test')

    def check_config(self, dev_id):
        if dev_id not in self.rules_dict.keys():
            self.rules_dict[dev_id] = load_config()

    def set(self, data):
        self.attr = AttrDict()
        self.attr['dev_id'] = data.get('devId')
        self.attr['dev_name'] = data.get('devName')
        self.check_config(data.get('devId'))

        self.attr['dev_rules'] = self.rules_dict.get(data.get('devId'))
        self.attr['dev_behavior'] = data.get('devBehavior')
        self.attr['integrate_model'] = data.get("isIntegrate")
        self.attr['duplicate_model'] = data.get("isDuplicate")
        self.attr['target_threshold'] = data.get('targetThreshold', 0)

        self.attr['face_handle'] = self.face_handle

        for dev_behavior_info in self.attr.dev_behavior:
            rules = self.attr.dev_rules
            alarm_time = dev_behavior_info.get("alarm_time")
            alarm_num = dev_behavior_info.get("alarm_num")
            behavior_number = dev_behavior_info.get("behavior_number")
            behavior_threshold = dev_behavior_info.get("behavior_threshold")
            rois = dev_behavior_info.get("rois_data")
            if alarm_time and not self.test:
                rules['behavior_' + str(behavior_number)]['alarm_time'] = int(alarm_time)
                rules['behavior_' + str(behavior_number)]['aiot_set'] = True  # 告警时加上时间
            if alarm_num and not self.test:
                rules['behavior_' + str(behavior_number)]['alarm_num'] = int(alarm_num)
            if behavior_threshold and not self.test:
                rules['behavior_' + str(behavior_number)]['thr'] = float(behavior_threshold)
            if self.activate:
                rules['behavior_' + str(behavior_number)]['alarm_time'] = 0
            self.attr['dev_rules'] = rules

            rois = rois if rois else None
            self.attr.dev_rules['behavior_' + str(behavior_number)]['rois'] = rois

        return self.attr

    def process(self, im, attr, out_result_dict):
        out_result_list = []
        out_package_boxes = []
        post_process_classes = dict()  # 用于告警视频

        for dtype_number_info in attr.dev_behavior:
            behavior_number = dtype_number_info.get("behavior_number")
            function = attr.dev_rules['behavior_' + str(behavior_number)].function
            kwargs = attr.dev_rules['behavior_' + str(behavior_number)].get('kwargs', {})

            thr = attr.dev_rules["behavior_" + str(behavior_number)].thr
            threshold = thr if thr > 0 else dtype_number_info.get("behavior_threshold")
            img_process = ImageProcess(im, attr.out_boxes, None, self.face_handle)
            target = attr.dev_rules["behavior_" + str(behavior_number)].target
            behavior_dict = {"target": target, "threshold": threshold, "behavior_number": behavior_number}
            attr.update(behavior_dict)

            img_process.dev_params = attr
            for fun in function:
                kws = kwargs.get(fun)
                create(fun, (img_process,), kws)
            self.rules_dict[attr.dev_id] = img_process.dev_params["dev_rules"]
            out_package_boxes.extend(img_process.boxes)
            post_process_classes[str(behavior_number)] = True if img_process.dev_params.roi_info_list else False
            if not img_process.behavior_result:
                continue
            behavior_result = img_process.behavior_result
            out_result_list.append(behavior_result)
            alarm_info = behavior_result.get('alarm_info')
            logger.info(f'{alarm_info}')
        out_result_dict['alarmBehavior'] = out_result_list
        out_result_dict['alarmBoxes'] = attr.out_boxes
        out_result_dict['alarmScores'] = attr.out_scores
        out_result_dict['alarmClasses'] = attr.out_classes
        out_result_dict['devId'] = attr.dev_id
        out_result_dict['devName'] = attr.dev_name
        out_result_dict['postprocessClasses'] = post_process_classes
        print(out_result_dict)
        attr['out_package_boxes'] = out_package_boxes
        if not self.test:
            logger.info(f'alarm classes: {attr.out_classes}')
            logger.info(f'alarm scores: {attr.out_scores}')
        # if out_result_list: logger.info(f'detect success: {out_result_list}')
        # logger.debug(f'当前摄像头{self.attr.dev_id}的全局变量规则为{self.rules_dict[self.attr.dev_id]}')

        return out_result_dict

    def predict(self, im, data, out_result_dict):
        """模型分析"""
        self.set(data)
        logger.info(f'predict ...')
        self.attr = self.detect.detect_image(im, self.attr)

    def pre_processing(self, im, data):
        out_result_dict = dict()
        if not data:
            return out_result_dict
        night = data.get("isNight")
        blur = data.get("isBlur")
        increase = data.get("isIncrease")
        dev_id = data.get('devId')
        move_threshold = data.get('moveThreshold')

        if move_threshold:
            move_flag = self.similarity.compute(im, dev_id, move_threshold)
            if move_flag: return out_result_dict

        if blur:
            blur_flag, _, _ = DeblurSelect.is_blur(im)
            if blur_flag: return out_result_dict

        if night:
            night_detection = NightVisionDetection()
            night_flag = night_detection.get_chroma(im)
            if night_flag: return out_result_dict

        return out_result_dict

    def post_processing(self, im, attr, out_result_dict):

        out_result_dict = self.process(im, attr, out_result_dict)
        out_result_dict = alarm_statistics(out_result_dict, attr)
        self.result_queue.put(out_result_dict)
        """
        dev_id = self.attr.get('devId')
        detect_type = self.attr.get("isDuplicate")
        mode = self.attr['dev_rules']['recognition_mode']
        if detect_type:
            if self.recognition_mode is None:
                self.recognition_mode = RecognitionMode()
            out_result_dict = self.recognition_mode.main(im, dev_id, out_result_dict, mode)

        if data.get("deBug"):
            HYPER_PARA.debug['behavior_number'] = data.get('devBehavior')[0].get("behavior_number")
            out_result_dict['alarmBehavior'].append(HYPER_PARA.debug)
        logger.info(f'result : {out_result_dict}')
        """

    def main(self, im, data):
        with contextlib.ExitStack() as stack:
            self.lock.acquire()
            stack.callback(self.lock.release)
            try:
                out_result_dict = self.pre_processing(im, data)
                self.predict(im, data, out_result_dict)

                if self.post_processing_thread is not None:
                    if not self.result_queue.empty():
                        out_result_dict = self.result_queue.get()

                if self.post_processing_thread is None or not self.post_processing_thread.is_alive():
                    self.post_processing_thread = threading.Thread(target=self.post_processing,
                                                                    args=(im, self.attr, out_result_dict))
                    self.post_processing_thread.start()

            except Exception as e:
                logger.exception(f'error: {e}')

        return out_result_dict
