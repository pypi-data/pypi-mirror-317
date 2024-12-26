# coding: utf-8
import threading
from queue import Queue
from ..utils.workspace import load_config
from ..analysis.occlusion_detect import occlusion_detect


class BaseDetectModel:
    def __init__(self, *args):
        self.model = None
        self.face_result = dict()
        self.occ_result = dict()
        self.data_queue = Queue()
        self.data_occ_queue = Queue()
        self.rules_dict = load_config()
        self.face_recognition_thread = None
        self.occlusion_detect_thread = None

        self._init()

    def _init(self):
        pass

    def face_recognition(self, im, dev_id, face_handle):
        face_boxes, face_scores, face_classes = face_handle.recognition(im)
        self.data_queue.put((dev_id, face_boxes, face_scores, face_classes))

    def occlusion_detect(self, im, dev_id, attr):
        boxes, scores, classes = occlusion_detect(im, attr)  # 5000011
        self.data_occ_queue.put((dev_id, boxes, scores, classes))

    def detect_image(self, im, attr):
        dev_id = attr.dev_id
        dev_behavior = attr.dev_behavior
        behavior_list = [str(behavior.get('behavior_number')) for behavior in dev_behavior]
        # object
        boxes, scores, classes = self.model.detect(im)

        # if '5000001' in behavior_list or '5000010' in behavior_list:
        # face
        alarm_face = []
        face_handle = attr['face_handle']
        alarm_num = attr['dev_rules']['behavior_5000010']['alarm_num']
        attr['dev_rules']['behavior_5000001']['target'] = face_handle.users

        face_boxes, face_scores, face_classes = [], [], []
        if self.face_recognition_thread is not None:
            if not self.data_queue.empty():
                face_result = self.data_queue.get()
                cam_id, face_boxes, face_scores, face_classes = face_result
                if dev_id == cam_id:
                    if len(face_classes) >= alarm_num and '5000010' in behavior_list:
                        boxes.extend(face_boxes)
                        scores.extend(face_scores)
                        classes.extend(['dual', 'dual'])
                    boxes.extend(face_boxes)
                    scores.extend(face_scores)
                    classes.extend(face_classes)
                elif self.face_result.get(dev_id):
                    face_boxes, face_scores, face_classes = self.face_result.get(dev_id)
                    if len(face_classes) >= alarm_num and '5000010' in behavior_list:
                        boxes.extend(face_boxes)
                        scores.extend(face_scores)
                        classes.extend(['dual', 'dual'])
                    boxes.extend(face_boxes)
                    scores.extend(face_scores)
                    classes.extend(face_classes)
                else:
                    self.face_result[dev_id] = (face_boxes, face_scores, face_classes)

        for bbox, score, cls in zip(face_boxes, face_scores, face_classes):
            data = {'name': cls, 'bbox': bbox}
            alarm_face.append(data)

        if self.face_recognition_thread is None or not self.face_recognition_thread.is_alive():
            self.face_recognition_thread = threading.Thread(target=self.face_recognition,
                                                            args=(im, dev_id, face_handle))
            self.face_recognition_thread.start()

        if '5000011' in behavior_list:
            if self.occlusion_detect_thread is not None:
                if not self.data_occ_queue.empty():
                    cam_id, occ_boxes, occ_scores, occ_classes = self.data_occ_queue.get()
                    if dev_id == cam_id:
                        boxes.extend(occ_boxes)
                        scores.extend(occ_scores)
                        classes.extend(occ_classes)
                    elif self.occ_result.get(dev_id):
                        occ_boxes, occ_scores, occ_classes = self.occ_result.get(dev_id)
                        boxes.extend(occ_boxes)
                        scores.extend(occ_scores)
                        classes.extend(occ_classes)
                    else:
                        self.occ_result[dev_id] = (occ_boxes, occ_scores, occ_classes)

            if self.occlusion_detect_thread is None or not self.occlusion_detect_thread.is_alive():
                self.occlusion_detect_thread = threading.Thread(target=self.occlusion_detect,
                                                                args=(im, dev_id, attr))
                self.occlusion_detect_thread.start()

        attr['out_boxes'] = boxes
        attr['out_scores'] = scores
        attr['out_classes'] = classes
        attr['alarm_face'] = alarm_face

        return attr
