# coding: utf-8
import os
import psutil
import hashlib
import numpy as np
from abc import ABC
from abc import abstractmethod
from .predictor import YoloOnnxModel
from .inference import BaseDetectModel
from .recognizer import BaseObjectDetect
from ..utils.base_utils import register
from ..utils.workspace import  create
from ..utils.logger import setup_logger
logger = setup_logger(__name__)


class LoadModel(object):
    """加载常规模型"""
    def __init__(self, cfg, **kwargs):
        self.onnx = YoloOnnxModel(cfg, **kwargs)()


class BaseModel(ABC):
    """模型初始化base类，需要实现__call__和detect方法"""
    @abstractmethod
    def __init__(self):
        self.model = None

    def __call__(self, test):
        self.check_finger()
        if test: self.check_time()

    @abstractmethod
    def detect(self, im):
        raise NotImplementedError(
            "需要重写BaseModel的detect函数")

    def check_finger(self):
        try:
            mac_addr = list()
            mac_addresses = {}
            addresses = psutil.net_if_addrs()
            for iface, addr_list in addresses.items():
                for addr in addr_list:
                    if addr.family == psutil.AF_LINK:
                        mac_addresses[iface] = addr.address

            for iface, mac in mac_addresses.items():mac_addr.append(mac)
            fingerprint = hashlib.sha256(''.join(mac_addr).encode('utf-8')).hexdigest()
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/onnx/version.txt'
            f = open(path, mode="r+")
            mac = f.readline()
            if fingerprint == mac:
                pass
                # logger.info('load detection model ...')
            else:
                logger.info('load detection model fail')
                exit(0)
        except Exception as e:
            logger.info('RuntimeError: Finger ')
            exit(0)

    def check_time(self):
        addr = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/onnx/time.txt'
        try:
            if not os.path.exists(addr):
                with open(addr, mode="w+") as f:
                    f.write('0')

            f = open(addr, mode="r+")
            dis = f.readline()
            if int(dis) > 100:
                logger.info('超过使用上限')
                exit(0)
            else:
                with open(addr, mode="w+") as f:
                    f.write(str(int(dis) + 1))
        except Exception as e:
            logger.info('RuntimeError: Time')
            exit(0)


@register
class DetectModel(BaseModel):
    def __init__(self):
        super().__init__()

    def __call__(self, rules_dict, **kwargs):
        super().__call__(kwargs.get('test'))
        self.model = LoadModel(rules_dict.onnx_models[0], **kwargs)
        im = np.zeros((1080, 1920, 3), dtype=np.uint8)
        self.model.onnx.detect(im)

        return self

    def detect(self, im):
        return self.model.onnx.detect(im)


class ObjectDetectModel(BaseDetectModel):
    def __init__(self, *args, **kwargs):
        super(ObjectDetectModel, self).__init__(*args)
        self.model = create(self.rules_dict.detect_mode,(self.rules_dict,), kws=kwargs)


class ObjectDetect(BaseObjectDetect):
    def __init__(self, *args, **kwargs):
        super(ObjectDetect, self).__init__(*args, **kwargs)
        self.detect = ObjectDetectModel(*args, **kwargs)