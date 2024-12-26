import os
import cv2
import queue
import threading
import copy
from zyapi.object_detection.models.builder import ObjectDetect
from zyapi.object_detection.utils.base_utils import draw_roi

cfg = {
        "devId": "000001",
        "devName": "沐曦测试摄像头",
        "filterType"
        "isNight": 0,
        "isBlur": 0,
        "isDuplicate": 0,
        "isIncrease": 0,
        "isIntegrate": 0,
        "moveThreshold": None,
        }

devBehavior = {
                '5000001':{
                    "behavior_number": 5000001,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000002': {
                    "behavior_number": 5000002,
                    "behavior_threshold": 0.3,
                    "alarm_num": 0,
                    "alarm_time": 0,
                    },
                '5000003': {
                    "behavior_number": 5000003,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000004': {
                    "behavior_number": 5000004,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000005': {
                    "behavior_number": 5000005,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000006': {
                    "behavior_number": 5000006,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000007': {
                    "behavior_number": 5000007,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000008': {
                    "behavior_number": 5000008,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000009': {
                    "behavior_number": 5000009,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    },
                '5000010': {
                    "behavior_number": 5000010,
                    "behavior_threshold": 0.5,
                    "alarm_num": 2,
                    "alarm_time": 0
                    },
                '5000011': {
                    "behavior_number": 5000011,
                    "behavior_threshold": 0.5,
                    "alarm_num": 0,
                    "alarm_time": 0
                    }
                }


class VisionEngin:
    def __init__(self, *args, test=True, cuda=False, activate=False, cache='/home/sweet/.mx/'):
        """
        算法测试类

        Args:
            args: 行参
            test: 默认为True(测试模式)，在测试模式下限制SDK的使用次数及写死类别阈值
            cuda: 默认False，如果为True，则调用CUDAExecutionProvider
            activate： 默认为False，如果为True，则alarm_time设置为0，识别即推送
            cache： 沐曦缓存模型地址
        """
        try:
            self.predict = ObjectDetect(*args, test=test, cuda=cuda, activate=activate, cache=cache)
            self.face_handle = self.predict.face_handle
            self.bev = devBehavior.keys()
            self.adds = list()
        except Exception as e:
            print('init failed')
            exit(0)

    def load_cfg(self, bev_list):
        bev = []
        for i in bev_list:
            bev.append(devBehavior[i])

        cfg['devBehavior'] = bev
        cfg['devId'] = str(len(self.adds))

        return cfg

    def test_video(self, addr, t=1, bev=None):
        self.adds.append(addr)
        if bev is None:
            bev = self.bev
        cfg = self.load_cfg(bev)
        save_path = './video_result/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        k = 0
        pic_num_read = 0
        camera = cv2.VideoCapture(addr)
        while camera.isOpened():
            ret, im = camera.read()
            if ret:
                pic_num_read = pic_num_read + 1
                if pic_num_read - k == t:
                    k = pic_num_read
                    result = self.predict.main(im, cfg)
                    result = result.get('alarmBehavior')
                    if result:
                        for behavior in result:
                            img = copy.copy(im)
                            out_result = behavior.get('result')
                            behavior_number = behavior.get('behavior_number')
                            alarm_info = behavior.get('alarm_info_dict').get('info_type')
                            # print(f'{behavior_number}--{alarm_info}')
                            for roi in out_result:
                                _roi = roi.get('roi')
                                boxes = roi.get('boxes')
                                img = draw_roi(img, _roi)

                                for index, bbox in enumerate(boxes):
                                    xx_min = int(bbox[0])
                                    yy_min = int(bbox[1])
                                    xx_max = int(bbox[2])
                                    yy_max = int(bbox[3])
                                    cv2.putText(img, str(behavior_number), (xx_min, yy_min),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                                    cv2.rectangle(img, (xx_min, yy_min), (xx_max, yy_max), (0, 255, 0), 3)

                            cv2.imwrite(save_path + '/' + alarm_info + '-' + str(pic_num_read) + '.jpg', img)
            else:
                break
        camera.release()

    def video_stream_capture(self, addr, frame_queue, mode):
        n = 0
        if int(mode) == 0:
            camera = cv2.VideoCapture(addr)
            while True:
                n += 1
                ret, frame = camera.read()
                if not ret:
                    print('rtsp restart...')
                    camera = cv2.VideoCapture(addr)
                    continue
                if frame_queue.full():
                    frame_queue.get()
                frame_queue.put((n, frame))
        else:
            while True:
                if frame_queue.empty():
                    n += 1
                    camera = cv2.VideoCapture(addr)
                    ret, frame = camera.read()
                    if ret:
                        frame_queue.put((n, frame))
                    camera.release()

    def process_frames(self, frame_queue, cfg, save_path):
        while True:
            try:
                n, im = frame_queue.get(timeout=5)
                result = self.predict.main(im, cfg)
                result = result.get('alarmBehavior')
                if result:
                    for behavior in result:
                        img = copy.copy(im)
                        out_result = behavior.get('result')
                        behavior_number = behavior.get('behavior_number')
                        alarm_info = behavior.get('alarm_info_dict').get('info_type')
                        # print(f'{behavior_number}--{alarm_info}')
                        for roi in out_result:
                            _roi = roi.get('roi')
                            boxes = roi.get('boxes')
                            img = draw_roi(img, _roi)

                            for index, bbox in enumerate(boxes):
                                xx_min = int(bbox[0])
                                yy_min = int(bbox[1])
                                xx_max = int(bbox[2])
                                yy_max = int(bbox[3])
                                cv2.putText(img, str(behavior_number), (xx_min, yy_min),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                                cv2.rectangle(img, (xx_min, yy_min), (xx_max, yy_max), (0, 255, 0), 3)

                        cv2.imwrite(save_path + '/' + alarm_info + '-' + str(n) + '.jpg', img)
                frame_queue.task_done()
            except queue.Empty:
                print('wait...')
                continue

    def test_rtsp(self, addr, mode=0, bev=None):
        if bev is None:
            bev = self.bev
        cfg = self.load_cfg(bev)
        save_path = './rtsp_result/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        frame_queue = queue.Queue(maxsize=1)

        capture_thread = threading.Thread(target=self.video_stream_capture, args=(addr, frame_queue, mode))
        capture_thread.start()

        process_thread = threading.Thread(target=self.process_frames, args=(frame_queue, cfg, save_path))
        process_thread.start()

        capture_thread.join()
        process_thread.join()

    def test_pic(self, addr, bev=None):
        if bev is None:
            bev = self.bev
        cfg = self.load_cfg(bev)
        save_path = './pic_result/'
        im = cv2.imread(addr)
        result = self.predict.main(im, cfg)
        result = result.get('alarmBehavior')
        if result:
            for behavior in result:
                img = copy.copy(im)
                out_result = behavior.get('result')
                behavior_number = behavior.get('behavior_number')
                alarm_info = behavior.get('alarm_info_dict').get('info_type')
                for roi in out_result:
                    _roi = roi.get('roi')
                    boxes = roi.get('boxes')
                    img = draw_roi(img, _roi)

                    for index, bbox in enumerate(boxes):
                        xx_min = int(bbox[0])
                        yy_min = int(bbox[1])
                        xx_max = int(bbox[2])
                        yy_max = int(bbox[3])
                        cv2.putText(img, str(behavior_number), (xx_min, yy_min),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                        cv2.rectangle(img, (xx_min, yy_min), (xx_max, yy_max), (0, 255, 0), 3)

                cv2.imwrite(save_path + '/' + alarm_info + '.jpg', img)

    def register(self, addr, name='沐曦'):
        im = cv2.imread(addr)

        info = self.face_handle.register(im, name)
        print(info)
