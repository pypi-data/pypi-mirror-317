import os
import cv2
import yaml
import time
import torch
import torchvision
import onnxruntime
import numpy as np
from sudtools import collection
from ..utils.logger import setup_logger
logger = setup_logger(__name__)


class YoloOnnxModel:
    def __init__(self, cfg, **kwargs):
        self.cfg = cfg
        self.conf = 0.25
        self.stride = 32
        self.cuda = kwargs.get('cuda', False)
        self.cache = kwargs.get('cache', '/home/sweet/.mx/')

    def __call__(self, device=0, size=(384, 640)):
        model = self.cfg['model']
        checkpoint = self.cfg['checkpoint']
        base_path = collection.model_dir()
        label_file = base_path + f'/{model}/labels.yml'
        with open(label_file) as f:
            file_cfg = yaml.load(f, Loader=yaml.Loader)

        self.device = device
        self.cat = file_cfg['labels']
        self.anchor = self.cfg['anchor']
        self.size = size if self.anchor else (640, 640)
        self.weight = base_path + f'/{model}/fp32_640.onnx' if self.cuda else base_path + f'/{model}/{checkpoint}.onnx'
        assert (os.path.exists(self.weight)), f"模型仓库里没有{self.weight}"

        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
        self.provider_options = [{'cache_mode': 0, 'cache_path': self.cache, 'prerun': 1}, {}]
        options = onnxruntime.SessionOptions()
        options.log_severity_level = 4
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.cuda else ['MacavxExecutionProvider', 'CPUExecutionProvider']
        if self.cuda:
            self.session = onnxruntime.InferenceSession(self.weight, sess_options=options, providers=self.providers)
        else:
            self.session = onnxruntime.InferenceSession(self.weight, sess_options=options, providers=self.providers, provider_options=self.provider_options)

        return self

    def from_numpy(self, x):
        return torch.from_numpy(x) if isinstance(x, np.ndarray) else x

    def box_area(self, box):
        return (box[2] - box[0]) * (box[3] - box[1])

    def xywh2xyxy(self, x):
        y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2
        y[:, 1] = x[:, 1] - x[:, 3] / 2
        y[:, 2] = x[:, 0] + x[:, 2] / 2
        y[:, 3] = x[:, 1] + x[:, 3] / 2
        return y

    def box_iou(self, box1, box2, eps=1e-7):
        (a1, a2), (b1, b2) = box1[:, None].chunk(2, 2), box2.chunk(2, 1)
        inter = (torch.min(a2, b2) - torch.max(a1, b1)).clamp(0).prod(2)
        return inter / (self.box_area(box1.T)[:, None] + self.box_area(box2.T) - inter + eps)

    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleup=True, stride=32):
        shape = im.shape[:2]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        elif isinstance(new_shape, list) and len(new_shape) == 1:
            new_shape = (new_shape[0], new_shape[1])

        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:
            r = min(r, 1.0)

        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        if auto:
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)
        dw /= 2
        dh /= 2

        if shape[::-1] != new_unpad:
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border

        if im.shape != (self.size[0], self.size[1], 3):
            im = cv2.resize(im, (self.size[1], self.size[0]))

        return im, r, (dw, dh)

    def clip_boxes(self, boxes, shape):
        if isinstance(boxes, torch.Tensor):
            boxes[..., 0].clamp(0, shape[1])
            boxes[..., 1].clamp(0, shape[0])
            boxes[..., 2].clamp(0, shape[1])
            boxes[..., 3].clamp(0, shape[0])
        else:
            boxes[..., [0, 2]] = boxes[..., [0, 2]].clip(0, shape[1])
            boxes[..., [1, 3]] = boxes[..., [1, 3]].clip(0, shape[0])

    def scale_boxes(self, img1_shape, boxes, img0_shape, ratio_pad=None, padding=True, xywh=False):
        if ratio_pad is None:
            gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])
            pad = (
                round((img1_shape[1] - img0_shape[1] * gain) / 2 - 0.1),
                round((img1_shape[0] - img0_shape[0] * gain) / 2 - 0.1),
            )
        else:
            gain = ratio_pad[0][0]
            pad = ratio_pad[1]

        if padding:
            boxes[..., 0] -= pad[0]
            boxes[..., 1] -= pad[1]
            if not xywh:
                boxes[..., 2] -= pad[0]
                boxes[..., 3] -= pad[1]
        boxes[..., :4] /= gain
        self.clip_boxes(boxes, img0_shape)
        return boxes

    def non_max_suppression(
            self,
            prediction,
            conf_thres=0.3,
            iou_thres=0.45,
            classes=None,
            agnostic=False,
            multi_label=False,
            labels=(),
            max_det=300,
            nm=0,
    ):

        if isinstance(prediction, (list, tuple)):
            prediction = prediction[0]

        device = prediction.device
        mps = 'mps' in device.type
        if mps:
            prediction = prediction.cpu()
        bs = prediction.shape[0]
        nc = prediction.shape[2] - nm - 5
        xc = prediction[..., 4] > conf_thres
        assert 0 <= conf_thres <= 1, f'{conf_thres}, 置信度阈值应该在0到1之间'
        assert 0 <= iou_thres <= 1, f'{iou_thres}, IOU阈值应该在0到1之间'

        max_wh = 4096
        max_nms = 30000
        time_limit = 0.5 + 0.05 * bs
        redundant = True
        multi_label &= nc > 1
        merge = False
        t = time.time()
        mi = 5 + nc
        output = [torch.zeros((0, 6 + nm), device=prediction.device)] * bs
        for xi, x in enumerate(prediction):
            x = x[xc[xi]]
            if labels and len(labels[xi]):
                lb = labels[xi]
                v = torch.zeros((len(lb), nc + nm + 5), device=x.device)
                v[:, :4] = lb[:, 1:5]
                v[:, 4] = 1.0
                v[range(len(lb)), lb[:, 0].long() + 5] = 1.0
                x = torch.cat((x, v), 0)
            if not x.shape[0]:
                continue
            x[:, 5:] *= x[:, 4:5]
            box = self.xywh2xyxy(x[:, :4])
            mask = x[:, mi:]
            if multi_label:
                i, j = (x[:, 5:mi] > conf_thres).nonzero(as_tuple=False).T
                x = torch.cat((box[i], x[i, 5 + j, None], j[:, None].float(), mask[i]), 1)
            else:
                conf, j = x[:, 5:mi].max(1, keepdim=True)
                x = torch.cat((box, conf, j.float(), mask), 1)[conf.view(-1) > conf_thres]

            if classes is not None:
                x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]

            n = x.shape[0]
            if not n:
                continue
            elif n > max_nms:
                x = x[x[:, 4].argsort(descending=True)[:max_nms]]
            else:
                x = x[x[:, 4].argsort(descending=True)]
            c = x[:, 5:6] * (0 if agnostic else max_wh)
            boxes, scores = x[:, :4] + c, x[:, 4]
            i = torchvision.ops.nms(boxes, scores, iou_thres)
            if i.shape[0] > max_det:
                i = i[:max_det]
            if merge and (1 < n < 3E3):
                iou = self.box_iou(boxes[i], boxes) > iou_thres
                weights = iou * scores[None]
                x[i, :4] = torch.mm(weights, x[:, :4]).float() / weights.sum(1, keepdim=True)
                if redundant:
                    i = i[iou.sum(1) > 1]
            output[xi] = x[i]
            if mps:
                output[xi] = output[xi].to(device)
            if (time.time() - t) > time_limit:
                logger.warning(f'NMS {time_limit:.3f}s')

        return output

    def preprocess(self, img):
        img = self.letterbox(img, self.size)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img)
        img = img.float()
        img /= 255
        if len(img.shape) == 3:
            img = img[None]
        img = img.cpu().numpy()

        return img

    def postprocess(self, preds, scale_shape, orig_shape):
        boxes = list()
        scores = list()
        classes = list()

        if self.anchor:
            pred = self.non_max_suppression(preds)
        else:
            mask = preds[..., 4] > self.conf
            pred = [p[mask[idx]] for idx, p in enumerate(preds)]
        det = pred[0]
        if len(det):
            det[:, :4] = self.scale_boxes(scale_shape, det[:, :4], orig_shape).round()
            for *xyxy, conf, cls in reversed(det):
                x_min = int(xyxy[0].item())
                y_min = int(xyxy[1].item())
                x_max = int(xyxy[2].item())
                y_max = int(xyxy[3].item())
                boxes.append([x_min, y_min, x_max, y_max])
                scores.append(float(conf))
                classes.append(self.cat[int(cls)])

        return boxes, scores, classes

    def detect(self, img):
        org_shape = img.shape
        img = self.preprocess(img)
        y = self.session.run(None, {self.session.get_inputs()[0].name: img})
        if isinstance(y, (list, tuple)):
            pred = self.from_numpy(y[0]) if len(y) == 1 else [self.from_numpy(x) for x in y]
        else:
            pred = self.from_numpy(y)

        boxes, scores, classes = self.postprocess(pred, img.shape[2:], org_shape)

        return boxes, scores, classes


if __name__ == '__main__':
    im = cv2.imread('/home/user/caizewu/code/project/zc/yolov10/ultralytics/assets/bus.jpg')
    rule_data = {'model': 'mx', 'checkpoint': 'fp16_640'}
    per = YoloOnnxModel(rule_data)()
    boxes, scores, classes = per.detect(im)
    print(boxes, scores, classes)
    for index, bbox in enumerate(boxes):
        xx_min = int(bbox[0])
        yy_min = int(bbox[1])
        xx_max = int(bbox[2])
        yy_max = int(bbox[3])
        cv2.putText(im, str(classes[index]), (xx_min, yy_min),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)
        cv2.rectangle(im, (xx_min, yy_min), (xx_max, yy_max), (0, 255, 0), 3)

    cv2.imshow('test', im)
    cv2.waitKey(0)
