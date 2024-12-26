import cv2
import time
import numpy as np
from .target import TargetRadius
from .utils import box2meas, state2box
from ...utils.parametar import HYPER_PARA

iou_thr = HYPER_PARA.iou_threshold
pix_thr = HYPER_PARA.pix_iou_threshold
move_thr = HYPER_PARA.move_threshold


class Camera:
    """每个摄像头一个Camera类, 每个Camera对象有多个TargetRadius类"""
    def __init__(self):
        self.state_list = []

    def run(self, boxes, classes):
        bbox_list_all, cls_list_all = boxes, classes
        mea_list = [box2meas(mea) for mea in bbox_list_all]
        if not mea_list:
            self.state_list = []
        unmatch_list, static_list, del_list = TargetRadius.association(self.state_list, mea_list, cls_list_all)
        self.state_list = [self.state_list[i] for i in range(len(self.state_list)) if i not in del_list]
        for idx in unmatch_list:
            self.state_list.append(TargetRadius(mea_list[idx], cls_list_all[idx], iou_thr, pix_thr))

        return static_list, unmatch_list, static_list, del_list


class RecognitionMode:
    """去除掉静止的目标.如果判断出某个类别的所有bbox都相对静止,则把该类别都删掉,否则不删除"""
    def __init__(self):
        self.runtime = 0
        self.result = None
        self.dev_id = {}
        self.move_id = {}

        self.unmatch_list = None
        self.static_list = None
        self.del_list = None

    def split(self, behavior_boxes, behavior_number):
        boxes = []
        classes = []

        boxes_list = np.array(behavior_boxes)
        boxes_list = boxes_list.reshape((-1, 4))
        for i in range(len(boxes_list)):
            bb = [int(boxes_list[i][0]), int(boxes_list[i][1]), int(boxes_list[i][2]), int(boxes_list[i][3])]
            boxes.append(bb)
            classes.append(str(behavior_number))
        return boxes, classes

    def check_boxes(self, out_result_dict):
        alarm_behavior_list = []
        alarm_behavior = out_result_dict.get('alarmBehavior')
        for k, behavior in enumerate(alarm_behavior):
            info_rois = ''
            result = list()
            out_result = behavior.get('result')
            if out_result:
                for v, roi_result in enumerate(out_result):
                    roi_name = roi_result.get('roi_name')
                    behavior_boxes = roi_result.get('boxes')
                    if behavior_boxes:
                        result.append(out_result[v])
                        if roi_name:
                            if not info_rois:
                                info_rois += roi_name
                            else:
                                info_rois += f'|{roi_name}'
                if result:
                    behavior['result'] = result
                    behavior['alarm_info'] = behavior['alarm_info_dict'].get('info_name') + info_rois + behavior['alarm_info_dict'].get('info_ftime') + \
                                             behavior['alarm_info_dict'].get('info_type')
                    behavior['alarm_info_dict']['info_rois'] = info_rois
                    alarm_behavior_list.append(behavior)

        out_result_dict['alarmBehavior'] = alarm_behavior_list

        return out_result_dict

    def target_radius(self, dev_id, out_result_dict):
        behavior_number_list = []
        alarm_behavior = out_result_dict.get('alarmBehavior')
        for k, behavior in enumerate(alarm_behavior):
            behavior_number = behavior.get('behavior_number')
            behavior_number_list.append(behavior_number)
            out_result = behavior.get('result')
            if out_result and int(behavior_number) not in [1002012, 1002023, 3003003]:
                roi_name_list = []
                for v, roi_result in enumerate(out_result):  # 循环result里面的区域
                    name = roi_result.get('roi_name')
                    roi_name_list.append(name)
                    behavior_boxes = roi_result.get('boxes')
                    boxes, classes = self.split(behavior_boxes, behavior_number)

                    start_time = time.time()
                    if dev_id not in self.dev_id.keys():
                        self.dev_id[dev_id] = {}
                    if behavior_number not in self.dev_id[dev_id].keys():
                        self.dev_id[dev_id][behavior_number] = {}
                    if name not in self.dev_id[dev_id][behavior_number].keys():
                        camera = Camera()
                        self.dev_id[dev_id][behavior_number][name] = camera
                        static_list, self.unmatch_list, self.static_list, self.del_list = camera.run(boxes, classes)
                    else:
                        static_list, self.unmatch_list, self.static_list, self.del_list = \
                        self.dev_id[dev_id][behavior_number][name].run(boxes, classes)
                        self.runtime = time.time() - start_time
                        if len(behavior_boxes) - 1 <= len(self.static_list) and len(
                                behavior_boxes) > 0:  # 同一类别同一roi所有目标都静止，则boxes赋值为[]
                            if name:
                                out_result_dict['alarmBehavior'][k]['result'][v]['boxes'] = []
                            else:
                                out_result_dict['alarmBehavior'][k]['result'] = []
                                out_result_dict['alarmBehavior'][k]['alarm_info'] = ''
                                out_result_dict['alarmBehavior'][k]['alarm_info_dict'] = {}
                del_roi_list = [list(self.dev_id[dev_id][behavior_number].keys())[i] for i in
                                range(len(self.dev_id[dev_id][behavior_number].keys())) if
                                list(self.dev_id[dev_id][behavior_number].keys())[i] not in roi_name_list]
                for name in del_roi_list:
                    self.dev_id[dev_id][behavior_number][name] = Camera()

                del_number_list = [list(self.dev_id[dev_id].keys())[i] for i in range(len(self.dev_id[dev_id].keys())) if
                                   list(self.dev_id[dev_id].keys())[i] not in behavior_number_list]
                for number in del_number_list:
                    self.dev_id[dev_id][number] = {}

        out_result_dict = self.check_boxes(out_result_dict)

        return out_result_dict

    def get_metrix(self, points):
        if points is None or len(points) < 2: return []

        x_l, y_l = [], []
        for point in points:
            x_l.append(point[0])
            y_l.append(point[1])
        x_min = int(min(x_l))
        x_max = int(max(x_l))
        y_min = int(min(y_l))
        y_max = int(max(y_l))

        return [x_min, y_min, x_max, y_max]

    def phash(self, img):
        img = cv2.resize(img, (50, 50))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.astype(np.float32)
        img = cv2.dct(img)
        img = img[0:10, 0:10]
        im_list = img.flatten().tolist()
        avg = sum(im_list) * 1 / len(im_list)
        avg_list = ['0' if i < avg else '1' for i in im_list]
        return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 100, 1)])

    def distance(self, hash1, hash2):
        count = 0
        assert len(hash1) == len(hash2)
        for i in range(len(hash1)):
            if hash1[i] != hash2[i]:
                count += 1
        return count

    def move_detect(self, im, dev_id, out_result_dict):
        if dev_id not in self.move_id.keys():
            self.move_id[dev_id] = {}
        alarm_behavior = out_result_dict.get('alarmBehavior')
        for k, behavior in enumerate(alarm_behavior):
            behavior_number = behavior.get('behavior_number')
            out_result = behavior.get('result')
            if behavior_number not in self.move_id[dev_id].keys():
                self.move_id[dev_id][behavior_number] = {}
            for v, roi_result in enumerate(out_result):
                roi_points = roi_result.get('roi')
                roi_name = roi_result.get('roi_name')

                roi_points = self.get_metrix(roi_points)
                roi_img = im[roi_points[1]:roi_points[3], roi_points[0]:roi_points[2]]
                hash1 = self.phash(roi_img)
                hash2 = self.move_id[dev_id][behavior_number].get(roi_name)
                count = self.distance(hash1, hash2) if hash2 else 100
                if count >= move_thr:
                    ...
                else:
                    out_result_dict['alarmBehavior'][k]['result'][v] = {}
                self.move_id[dev_id][behavior_number][roi_name] = hash1

        out_result_dict = self.check_boxes(out_result_dict)

        return out_result_dict

    def main(self, im, dev_id, out_result_dict, mode):
        """
        description: 主函数,传入

        param:
            json_data:  json字符串
            out_result_dict： 识别结果
        return:
            返回去除掉静止目标的classes scores boxes
        """
        if not out_result_dict.get('alarmBehavior'):
            self.dev_id[dev_id] = {}
            return out_result_dict

        if mode == 'TargetRadius':
            out_result_dict = self.target_radius(dev_id, out_result_dict)
        else:
            out_result_dict = self.move_detect(im, dev_id, out_result_dict)

        return out_result_dict


if __name__ == '__main__':
    test_data = [{
        "dev_id": "123",
        "dev_no": "0001",
        "img": [],
        "dev_behavior": {
            "behavior_name": ["unsafehel"],
            "behavior_number": [1002001],
            "behavior_threshold": ["0.3"]
        },
        "dev_data": [
            {
                "someone": True,
                "unmanned": False,
                "night": True,
                "increase": True,
                "fast": False,
                "filter": True,
                "object_size": "1920,1080",
            }
        ],
        "ROI": [
            {
                "name": "unsafehel",
                "number": "1002001",
                "data": []
            }
        ]
    },
        {
            "dev_id": "123",
            "dev_no": "0001",
            "img": [],
            "dev_behavior": {
                "behavior_name": ["unsafehel"],
                "behavior_number": [1002001],
                "behavior_threshold": ["0.3"]
            },
            "dev_data": [
                {
                    "someone": True,
                    "unmanned": False,
                    "night": True,
                    "increase": True,
                    "fast": False,
                    "filter": True,
                    "object_size": "1920,1080",
                }
            ],
            "ROI": [
                {
                    "name": "unsafehel",
                    "number": "1002001",
                    "data": []
                }
            ]
        },
        {
            "dev_id": "456",
            "dev_no": "0001",
            "img": [],
            "dev_behavior": {
                "behavior_name": ["unsafehel"],
                "behavior_number": [1002001],
                "behavior_threshold": ["0.3"]
            },
            "dev_data": [
                {
                    "someone": True,
                    "unmanned": False,
                    "night": True,
                    "increase": True,
                    "fast": False,
                    "filter": True,
                    "object_size": "1920,1080",
                }
            ],
            "ROI": [
                {
                    "name": "unsafehel",
                    "number": "1002001",
                    "data": []
                }
            ]
        }
    ]

    data1 = {'behavior': [{'behavior_number': 1002001,
                           'boxes': [[920, 232, 1007, 304, '1002001', '0.33453431725502014'],
                                     [781, 491, 895, 604, '1002001', '0.8324827551841736'],
                                     [1367, 374, 1450, 470, '1002001', '0.8513033986091614'],
                                     [1763, 886, 1895, 1028, '1002001', '0.8540068864822388'],
                                     [518, 303, 591, 387, '1002001', '0.8638141751289368'],
                                     [767, 405, 859, 503, '1002001', '0.8727522492408752']], 'person_number': 5},
                          {'behavior_number': 1002006,
                           'boxes': [[920, 232, 1007, 304, '1002006', '0.33453431725502014'],
                                     [781, 491, 895, 604, '1002006', '0.8324827551841736'],
                                     [1367, 374, 1450, 470, '1002006', '0.8513033986091614'],
                                     [1763, 886, 1895, 1028, '1002006', '0.8540068864822388'],
                                     [518, 303, 591, 387, '1002006', '0.8638141751289368'],
                                     [767, 405, 859, 503, '1002006', '0.8727522492408752']], 'person_number': 5
                          }
                           ],
             'boxes': [[[707.0, 426.0, 964.0, 772.0], [619.0, 384.0, 866.0, 819.0], [920.0, 232.0, 1007.0, 304.0],
                        [772.0, 550.0, 1015.0, 764.0], [1310.0, 425.0, 1484.0, 601.0], [1573.0, 888.0, 1901.0, 1080.0],
                        [763.0, 488.0, 1054.0, 831.0], [478.0, 301.0, 737.0, 835.0], [1305.0, 375.0, 1488.0, 612.0],
                        [781.0, 491.0, 895.0, 604.0], [1367.0, 374.0, 1450.0, 470.0], [1763.0, 886.0, 1895.0, 1028.0],
                        [518.0, 303.0, 591.0, 387.0], [767.0, 405.0, 859.0, 503.0]],
                       [0.2887134552001953, 0.3195984661579132, 0.33453431725502014, 0.3960975706577301,
                        0.5204468369483948, 0.6030586361885071, 0.6653063297271729, 0.7433191537857056,
                        0.8148852586746216, 0.8324827551841736, 0.8513033986091614, 0.8540068864822388,
                        0.8638141751289368, 0.8727522492408752],
                       ['otherperson', 'otherperson', 'unsafehel', 'inapprodress', 'inapprodress', 'otherperson',
                        'otherperson', 'otherperson', 'otherperson', 'unsafehel', 'unsafehel', 'unsafehel', 'unsafehel',
                        'unsafehel']]}
    data2 = {'behavior': [{'behavior_number': 1002001,
                           'boxes': [[920, 232, 1007, 304, '1002001', '0.33453431725502014'],
                                     [781, 491, 895, 604, '1002001', '0.8324827551841736'],
                                     [1367, 374, 1450, 470, '1002001', '0.8513033986091614'],
                                     [1763, 886, 1895, 1028, '1002001', '0.8540068864822388'],
                                     [518, 303, 591, 387, '1002001', '0.8638141751289368'],
                                     [767, 405, 859, 503, '1002001', '0.8727522492408752']], 'person_number': 5},
                          {'behavior_number': 1002006,
                           'boxes': [[920, 232, 1007, 304, '1002006', '0.33453431725502014'],
                                     [781, 491, 895, 604, '1002006', '0.8324827551841736'],
                                     [1367, 374, 1450, 470, '1002006', '0.8513033986091614'],
                                     [1763, 886, 1895, 1028, '1002006', '0.8540068864822388'],
                                     [518, 303, 591, 387, '1002006', '0.8638141751289368'],
                                     [167, 205, 259, 303, '1002006', '0.8727522492408752']], 'person_number': 5
                           }
                          ],
             'boxes': [[[707.0, 426.0, 964.0, 772.0], [619.0, 384.0, 866.0, 819.0], [920.0, 232.0, 1007.0, 304.0],
                        [772.0, 550.0, 1015.0, 764.0], [1310.0, 425.0, 1484.0, 601.0], [1573.0, 888.0, 1901.0, 1080.0],
                        [763.0, 488.0, 1054.0, 831.0], [478.0, 301.0, 737.0, 835.0], [1305.0, 375.0, 1488.0, 612.0],
                        [781.0, 491.0, 895.0, 604.0], [1367.0, 374.0, 1450.0, 470.0], [1763.0, 886.0, 1895.0, 1028.0],
                        [518.0, 303.0, 591.0, 387.0], [767.0, 405.0, 859.0, 503.0]],
                       [0.2887134552001953, 0.3195984661579132, 0.33453431725502014, 0.3960975706577301,
                        0.5204468369483948, 0.6030586361885071, 0.6653063297271729, 0.7433191537857056,
                        0.8148852586746216, 0.8324827551841736, 0.8513033986091614, 0.8540068864822388,
                        0.8638141751289368, 0.8727522492408752],
                       ['otherperson', 'otherperson', 'unsafehel', 'inapprodress', 'inapprodress', 'otherperson',
                        'otherperson', 'otherperson', 'otherperson', 'unsafehel', 'unsafehel', 'unsafehel', 'unsafehel',
                        'unsafehel']]}
    data3 = {'behavior': [{'behavior_number': 1002001,
                           'boxes': [[920, 232, 1007, 304, '1002001', '0.33453431725502014'],
                                     [781, 491, 895, 604, '1002001', '0.8324827551841736'],
                                     [1367, 374, 1450, 470, '1002001', '0.8513033986091614'],
                                     [1763, 886, 1895, 1028, '1002001', '0.8540068864822388'],
                                     [518, 303, 591, 387, '1002001', '0.8638141751289368'],
                                     [767, 405, 859, 503, '1002001', '0.8727522492408752']], 'person_number': 5}],
             'boxes': [[[707.0, 426.0, 964.0, 772.0], [619.0, 384.0, 866.0, 819.0], [920.0, 232.0, 1007.0, 304.0],
                        [772.0, 550.0, 1015.0, 764.0], [1310.0, 425.0, 1484.0, 601.0], [1573.0, 888.0, 1901.0, 1080.0],
                        [763.0, 488.0, 1054.0, 831.0], [478.0, 301.0, 737.0, 835.0], [1305.0, 375.0, 1488.0, 612.0],
                        [781.0, 491.0, 895.0, 604.0], [1367.0, 374.0, 1450.0, 470.0], [1763.0, 886.0, 1895.0, 1028.0],
                        [518.0, 303.0, 591.0, 387.0], [767.0, 405.0, 859.0, 503.0]],
                       [0.2887134552001953, 0.3195984661579132, 0.33453431725502014, 0.3960975706577301,
                        0.5204468369483948, 0.6030586361885071, 0.6653063297271729, 0.7433191537857056,
                        0.8148852586746216, 0.8324827551841736, 0.8513033986091614, 0.8540068864822388,
                        0.8638141751289368, 0.8727522492408752],
                       ['otherperson', 'otherperson', 'unsafehel', 'inapprodress', 'inapprodress', 'otherperson',
                        'otherperson', 'otherperson', 'otherperson', 'unsafehel', 'unsafehel', 'unsafehel', 'unsafehel',
                        'unsafehel']]}
    data = [data1, data2, data3]
    recognition_mode = RecognitionMode()

    for i, json_data in enumerate(test_data):
        result = recognition_mode.main(json_data, data[i])
        print('--------------分析----------------')
        print('摄像头id：', json_data['dev_id'])
        print('相对静止的目标：', recognition_mode.static_list)
        print('出了画面的目标：', recognition_mode.del_list)
        print('画面中新出现或者移动速度过快或者新增的摄像头，导致的新增目标：', recognition_mode.unmatch_list)
        print('去除掉静止不动的目标后，剩余的目标：', result)
        print('总耗时：', recognition_mode.runtime)
        print('----------------------------------')
