# coding: utf-8
import time
import cv2
import copy
import datetime
import uuid
import hashlib
import platform
import numpy as np
import networkx as nx

from .workspace import register
from shapely.geometry import Polygon, MultiPoint


def coordinate_sort(scores_index_list, out_boxes, out_scores, out_classes):
    """
    坐标排序

    Args:
        scores_index_list: 阈值符合的索引
        out_boxes: 识别结果坐标
        out_scores: 识别结果阈值
        out_classes: 识别结果类别
    Return:
        out_boxes_list: 排序后的boxes
        out_scores_list: 排序后的scores
        out_classes_list: 排序后的classes
    """
    out_boxes_list = []
    out_scores_list = []
    out_classes_list = []
    if scores_index_list:
        for box in scores_index_list:
            out_boxes_list.append(out_boxes[int(box)])
            out_scores_list.append(out_scores[int(box)])
            out_classes_list.append(out_classes[int(box)])
        return out_boxes_list, out_scores_list, out_classes_list
    else:
        return out_boxes_list, out_scores_list, out_classes_list


def target_size_filter(bbox, thr):
    """
    根据阈值，筛选符合大小的目标

    Args:
        bbox: 目标框
        thr: 阈值

    """
    # 筛选出符合阈值的目标
    if (bbox[2] - bbox[0] + bbox[3] - bbox[1]) / 2 > thr:
        return True
    else:
        return False


def merge_bbox_flag(coordinates, thr=0.5):
    """
    两个目标是否重叠

    Args:
        coordinates: np.array, 待计算两个目标的坐标值
        thr: IOU阈值
    Return:
        True or False
    """
    flag = False
    if len(coordinates) == 0:
        return flag

    x1 = coordinates[:, 0]
    y1 = coordinates[:, 1]
    x2 = coordinates[:, 2]
    y2 = coordinates[:, 3]

    xx1 = np.maximum(x1[0], x1[1])
    yy1 = np.maximum(y1[0], y1[1])
    xx2 = np.minimum(x2[0], x2[1])
    yy2 = np.minimum(y2[0], y2[1])

    w = np.maximum(0.0, xx2 - xx1 + 1)
    h = np.maximum(0.0, yy2 - yy1 + 1)
    inter = w * h
    if (inter / ((x2[0] - x1[0]) * (y2[0] - y1[0]))) > thr:
        flag = True
    return flag


def roi_area(point_list):
    """
    计算设置区域的四边形面积

    Args:
        point_list: list，例如[[969, 79], [1556, 60], [1556, 517], [924, 608]]
    Return:
        line_box: 多边形左边的ndarray
        poly: Polygon对象
        area: 多边形面积
    """
    line_box = np.array(point_list).reshape(len(point_list)//2, 2)  # 多边形边形二维坐标表示
    poly = Polygon(line_box)  # python四边形对象，会自动计算四个点，最后四个点顺序为：左上 左下  右下 右上 左上
    poly = poly.buffer(0.01)
    area = poly.area

    return line_box, poly, area


def check_overlapped_area(roi, box, overlap=0.6):
    """
    计算设置区域的四边形面积

    Args:
        point_list：list，例如[[969, 79], [1556, 60], [1556, 517], [924, 608]]
    Return:
        line_box: 多边形左边的ndarray
        poly: Polygon对象
        area: 多边形面积
    """
    is_overlapped = False
    points = []  # roi转为顶点坐标列表
    for point in roi:
        for item in point:
            points.append(item)

    line_roi, poly_roi, area_roi = roi_area(points)  # 获取ROI:线框，多边形、面积

    x1, y1, x2, y2, x3, y3, x4, y4 = box[0], box[1], box[2], box[1], box[2], box[3], box[0], box[3]

    point_list = [x1, y1, x4, y4, x3, y3, x2, y2]  # 顶点坐标转换 顺序:左上,左下,右下,右上
    line_box, poly_box, area_box = roi_area(point_list)  # 获取BOX:线框，多边形、面积

    if not poly_roi.intersects(poly_box): return is_overlapped  # 如果两四边形不相交，继续下个roi区域判读

    union_poly = np.concatenate((line_roi, line_box))  # 合并两个box坐标，变为8*2
    inter_area = poly_roi.intersection(poly_box).area  # 相交面积
    union_area = MultiPoint(union_poly).convex_hull.area
    if union_area != 0:  # 有相交的情况
        if area_roi > area_box:
            iou = float(inter_area) / area_box
        else:
            iou = float(inter_area) / area_roi
        if iou > overlap:  # 相交面积与当前对象面积比例大于overlap
            is_overlapped = True

    return is_overlapped


def cal_iou(state, measure):
    s_tl_x, s_tl_y, s_br_x, s_br_y = state[0], state[1], state[2], state[3]
    m_tl_x, m_tl_y, m_br_x, m_br_y = measure[0], measure[1], measure[2], measure[3]
    # 计算相交部分的坐标
    x_min = max(s_tl_x, m_tl_x)
    x_max = min(s_br_x, m_br_x)
    y_min = max(s_tl_y, m_tl_y)
    y_max = min(s_br_y, m_br_y)
    inter_h = max(y_max - y_min + 1, 0)
    inter_w = max(x_max - x_min + 1, 0)
    inter = inter_h * inter_w
    x_min_ = min(s_tl_x, m_tl_x)
    x_max_ = max(s_br_x, m_br_x)
    y_min_ = min(s_tl_y, m_tl_y)
    y_max_ = max(s_br_y, m_br_y)
    if inter == 0:
        return 0
    else:
        return inter / ((x_max_ - x_min_) * (y_max_ - y_min_))


def match(state_list, measure_list):
    state_rec = {i for i in range(len(state_list))}
    mea_rec = {i for i in range(len(measure_list))}
    graph = nx.Graph()
    for idx_sta, state in enumerate(state_list):
        state_node = 'state_%d' % idx_sta
        graph.add_node(state_node, bipartite=0)
        for idx_mea, measure in enumerate(measure_list):
            mea_node = 'mea_%d' % idx_mea
            graph.add_node(mea_node, bipartite=1)
            score = cal_iou(state, measure)

            if score is not None:
                graph.add_edge(state_node, mea_node, weight=score)
    match_set = nx.max_weight_matching(graph)
    res = dict()
    for (node_1, node_2) in match_set:
        if node_1.split('_')[0] == 'mea':
            node_1, node_2 = node_2, node_1
        res[node_1] = node_2

    state_used_list = list()
    mea_used_list = list()
    state_used = set()
    mea_used = set()
    mea_unmatch_list = list()
    state_unmatch_list = list()
    for state, mea in res.items():
        state_index = int(state.split('_')[1])
        mea_index = int(mea.split('_')[1])
        mea_used.add(mea_index)
        state_used.add(state_index)
        mea_used_list.append(mea_index)
        state_used_list.append(state_index)

    for mea_new in list(mea_rec - mea_used):
        mea_unmatch_list.append(mea_new)

    for state_now in list(state_rec - state_used):
        state_unmatch_list.append(state_now)
    return state_used_list, mea_used_list, state_unmatch_list, mea_unmatch_list


def alarm_statistics(out_result_dict, attr):
    """
    计算每个行为的告警数量

    Args:
        out_result_dict: 整合后的结果
        attr
    Returns:
        将person_number加入到out_result中
    """
    alarm_statistics_list = []
    data = out_result_dict.get('alarmBehavior')
    if not data:
        return out_result_dict
    sample_behavior = attr.get('dev_rules').keys()
    for behavior in sample_behavior:
        if 'behavior' in behavior:
            alarm_statistics_list.append(int(behavior[9:]))
    for index, behavior in enumerate(data):
        alarm_number = 0
        behavior_number = behavior['behavior_number']
        out_result = behavior['result']
        if behavior_number in alarm_statistics_list:
            if str(behavior_number) in ['1002014']:
                bbox = []
                alarm_num = attr.get('dev_rules').get('behavior_1002014').get('alarm_num')
                for v, roi_result in enumerate(out_result):
                    behavior_boxes = roi_result.get('boxes')
                    bbox += behavior_boxes
                if len(bbox) >= int(alarm_num):
                    alarm_number = len(bbox) - int(alarm_num)
            elif str(behavior_number) in ['1002015']:
                bbox = []
                alarm_num = attr.get('dev_rules').get('behavior_1002015').get('alarm_num')
                for v, roi_result in enumerate(out_result):
                    behavior_boxes = roi_result.get('boxes')
                    bbox += behavior_boxes
                if bbox:
                    alarm_number = int(alarm_num) - len(bbox)
            elif str(behavior_number) in ['1002010']:
                # TODO:回头加上
                pass
            else:
                bbox = []
                for v, roi_result in enumerate(out_result):
                    behavior_boxes = roi_result.get('boxes')
                    bbox += behavior_boxes
                alarm_number = len(bbox)
        out_result_dict['alarmBehavior'][index]['amount'] = alarm_number

    return out_result_dict


def draw_bbox(out_boxes, out_scores, out_classes, im):
    """画图"""
    for ii in range(len(out_classes)):
        xx_min = int(out_boxes[ii][0])
        yy_min = int(out_boxes[ii][1])
        xx_max = int(out_boxes[ii][2])
        yy_max = int(out_boxes[ii][3])
        if out_classes[ii] in ['unsafehel'] and out_scores[ii] > 0.7:
            cv2.rectangle(im, (xx_min, yy_min), (xx_max, yy_max), (0, 255, 0), 3)
            cv2.putText(im, str(out_classes[ii]) + '|' + str(out_scores[ii]), (xx_min, yy_min),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)
            # cv2.putText(im, scores[i], (x_min, y_min + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color[classes[i]], 1)
    cv2.namedWindow('test', 0)
    cv2.resizeWindow("test", 1000, 1000)
    cv2.imshow('test', im)
    cv2.waitKey(0)


def draw_roi(img, roi_list):
    """将区域画在图片上"""
    alpha = 0.8
    beta = 1-alpha
    gamma = 0
    for roi in roi_list:
        pts = np.array(roi, np.int32)
        pts = pts.reshape((-1, 1, 2))
        img_new = img.copy()
        cv2.fillPoly(img_new, [pts], (255, 255, 0))  # 在新图片上填充画框
        img = cv2.addWeighted(img, alpha, img_new, beta, gamma)
    return img


def get_hardware_fingerprint():
    info = list()
    info.append(str(uuid.getnode()))
    info.append(platform.machine())
    info.append(platform.processor())
    info.append(platform.system())

    fingerprint = hashlib.sha256(''.join(info).encode('utf-8')).hexdigest()

    return fingerprint


def get_current_time():
    """返回当前世界时间, 用于算法行为的开始时间和结果时间"""
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    sencod = datetime.datetime.now().second

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    t = (str(hour), str(min), str(sencod))
    now_time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + (':').join(t)
    now_strptime = time.mktime(time.strptime(now_time, '%Y-%m-%d %H:%M:%S'))

    return int(now_strptime)


def get_specific_time(specific_time):
    """返回当前世界时间, 用于算法行为的开始时间和结果时间"""
    hour = specific_time[0:2]
    min = specific_time[3:]
    second = '00'

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    t = (str(hour), str(min), str(second))
    now_time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + (':').join(t)
    now_strptime = time.mktime(time.strptime(now_time, '%Y-%m-%d %H:%M:%S'))

    return int(now_strptime)


def is_working(detect_time):
    """判断是否在工作日的工作时间内"""
    from chinese_calendar import is_workday
    data = datetime.datetime.now().date()
    now_time = datetime.datetime.now()
    am_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + detect_time[0], '%Y-%m-%d%H:%M')
    am_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + detect_time[1], '%Y-%m-%d%H:%M')
    pm_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + detect_time[2], '%Y-%m-%d%H:%M')
    pm_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + detect_time[3], '%Y-%m-%d%H:%M')
    if is_workday(data):
        if am_start_time < now_time < am_end_time or pm_start_time < now_time < pm_end_time:
            return True
        else:
            return False
    else:
        return False


@register
def target_filter(img_process):
    """
    根据阈值，筛选符合的目标

    Args:
        img_process: 所需参数

    """
    dev_params = img_process.dev_params
    target_threshold = dev_params.target_threshold
    # 保存识别到的结果索引值
    index_list = []
    boxes_dict = {}
    scores_dict = {}
    classes_dict = {}
    for i, label in enumerate(dev_params.target):
        # 如果识别行为在返回结果中
        boxes_dict[label] = []
        scores_dict[label] = []
        classes_dict[label] = []
        if label in dev_params.out_classes:
            for index, classes in enumerate(dev_params.out_classes):
                if label == classes and dev_params.out_scores[index] > dev_params.threshold and target_size_filter(dev_params.out_boxes[index], target_threshold):
                    index_list.append(index)
                    boxes_dict[label].append(list(dev_params.out_boxes[index]))
                    scores_dict[label].append(dev_params.out_scores[index])
                    classes_dict[label].append(dev_params.out_classes[index])

    # 符合阈值的索引值
    scores_index_list = img_process.threshold_filter(index_list, dev_params.out_scores, dev_params.threshold)

    # 拿到合适的坐标,进行返回
    out_boxes_list, out_scores_list, out_classes_list = coordinate_sort(scores_index_list, dev_params.out_boxes, dev_params.out_scores, dev_params.out_classes)

    dev_params['out_boxes_list'] = out_boxes_list
    dev_params['out_scores_list'] = out_scores_list
    dev_params['out_classes_list'] = out_classes_list
    dev_params['out_boxes_dict'] = boxes_dict
    dev_params['out_scores_dict'] = scores_dict
    dev_params['out_classes_dict'] = classes_dict
    img_process.dev_params = dev_params


@register
def post_process(img_process, behavior=None, iou=0.1):
    """
    后处理部分

    Args:
        img_process: 后处理类
        behavior: 行为编号
        iou (float): iou值
    Return:
        经过后处理逻辑的out_result字典
    """
    # 后处理
    out_boxes_list = []
    out_scores_list = []
    out_classes_list = []

    dev_params = img_process.dev_params
    out_boxes_dict = dev_params['out_boxes_dict']
    out_scores_dict = dev_params['out_scores_dict']
    out_classes_dict = dev_params['out_classes_dict']

    if behavior in ['5000002']:
        if len(out_boxes_dict[dev_params.target[0]]) > 0:
            cleye_boxes_list = out_boxes_dict[dev_params.target[0]]
            cleye_score_list = out_scores_dict[dev_params.target[0]]
            cleye_classes_list = out_classes_dict[dev_params.target[0]]

            other_boxes_list = out_boxes_dict[dev_params.target[1]] + out_boxes_dict[dev_params.target[2]] + out_boxes_dict[dev_params.target[3]]
            if len(other_boxes_list) == 0:
                out_boxes_list.extend(cleye_boxes_list)
                out_scores_list.extend(cleye_score_list)
                out_classes_list.extend(cleye_classes_list)
    if behavior in ['5000011']:
        if len(out_boxes_dict[dev_params.target[0]]) > 0:
            occ_boxes_list = out_boxes_dict[dev_params.target[0]]
            occ_score_list = out_scores_dict[dev_params.target[0]]
            occ_classes_list = out_classes_dict[dev_params.target[0]]

            other_boxes_list = out_boxes_dict[dev_params.target[1]] + out_boxes_dict[dev_params.target[2]] + out_boxes_dict[dev_params.target[3]] + out_boxes_dict[dev_params.target[4]]
            if len(other_boxes_list) == 0:
                out_boxes_list.extend(occ_boxes_list)
                out_scores_list.extend(occ_score_list)
                out_classes_list.extend(occ_classes_list)

    index = [i for i in range(len(out_boxes_list))]
    scores_index_list = img_process.threshold_filter(index, out_scores_list, dev_params.threshold)

    # 拿到合适的坐标,进行返回
    out_boxes_list, out_scores_list, out_classes_list = coordinate_sort(scores_index_list, out_boxes_list, out_scores_list, out_classes_list)

    dev_params['out_boxes_list'] = out_boxes_list
    dev_params['out_scores_list'] = out_scores_list
    dev_params['out_classes_list'] = out_classes_list
    img_process.dev_params = dev_params

    return dev_params


@register
def package_bbox(img_process):
    """包装bbox"""
    kwargs = img_process.dev_params
    out_boxes_list = kwargs.get('out_boxes_list')
    out_scores_list = kwargs.get('out_scores_list')
    out_classes_list = kwargs.get('out_classes_list')
    behavior_number = kwargs.get('behavior_number')
    result = list()
    # 整理坐标位置
    for index, box in enumerate(out_boxes_list):
        box_list = list()
        box_list.append(int(box[0]))
        box_list.append(int(box[1]))
        box_list.append(int(box[2]))
        box_list.append(int(box[3]))
        box_list.append(str(behavior_number))
        box_list.append(str(out_scores_list[index]))
        box_list.append(str(out_classes_list[index]))
        result.append(box_list)
    img_process.boxes = result


@register
def check_bbox(img_process):
    """针对连续识别n分钟才告警的场景，根据mode判断bbox是在roi之外or之内"""
    # 获取当前摄像头的roi区域
    kwargs = img_process.dev_params
    behavior_number = kwargs.get('behavior_number')
    rules = kwargs.get('dev_rules')
    state = rules.get('behavior_' + str(behavior_number)).get('mode')
    rois = copy.deepcopy(rules.get('behavior_' + str(behavior_number)).rois)
    if rois is None:  # 如果没有设置ROI，则在全图内检测，想要立马告警，alarm_time设成0
        h, w = img_process.image.shape[0:2]
        rois = [{'roi_name': None, 'roi': [[0, 0], [0, h], [w, h], [w, 0]]}]  # name为区域名称
    img_process.roi_list = rois
    if rois:  # 如果设置了ROI，则在ROI区域内检测
        if state == 'half_out':
            img_process.ele_fence_mode = state
            out_boxes_list, roi_info_list = img_process.check_point_in_area("out")
        elif state == 'klx_out':
            img_process.ele_fence_mode = state
            out_boxes_list, roi_info_list = img_process.check_point_in_area("out")
        elif state == 'half_in':
            img_process.ele_fence_mode = state
            out_boxes_list, roi_info_list = img_process.check_point_in_area("in")
        elif state == 'overlap_in':  # 通过重叠面积判断是否在roi区域里
            img_process.ele_fence_mode = state
            out_boxes_list, roi_info_list = img_process.check_point_in_area("in")

    img_process.face_boxes = out_boxes_list  # 用于人脸
    img_process.out_boxes = out_boxes_list  # 行为数量统计时使用
    img_process.alarm_info = ''

    kwargs['roi_info_list'] = roi_info_list  # 每个roi下面符合的bbox
    img_process.dev_params = kwargs


@register
def check_ftime(img_process):
    """
    增加时间判断，当某个行为连续持续alarm_time分钟，则推送告警信息，需要结合roi区域
    Args:
        img_process (dict): img_process类
    Return:
        detect_info + info_add_list (list): 用于更新behavior_info
        out_result (dict): 过滤后的结果
    """
    kwargs = img_process.dev_params
    roi_info_list = kwargs.get('roi_info_list')
    behavior_number = kwargs.get('behavior_number')
    dev_name = kwargs.get('dev_name')
    wait_time = kwargs.get('dev_rules').get('wait_time')
    alarm_time = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('alarm_time')
    detect_info = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('detect_info')
    rate = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('rate')
    face_info = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('face_info')
    behavior_info = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('behavior_info')
    aiot_set = kwargs.get('dev_rules').get('behavior_' + str(behavior_number)).get('aiot_set')
    now_strptime = get_current_time()

    alarm_info = ''
    alarm_ftime_info = ''
    alarm_info_dict = dict()
    alarm_info_dict['info_name'] = f'在{dev_name}'
    alarm_info_dict['info_rois'] = ''
    alarm_info_dict['info_ftime'] = ''
    alarm_info_dict['info_type'] = f'检测到{behavior_info}'
    out_result = []  # 要保存在img_process.out_result中
    out_boxes = []
    face_result = []
    info_del_list = []
    info_add_list = []
    if detect_info is None or len(detect_info) == 0:
        detect_info = []
        for index, item in enumerate(roi_info_list):  # roi_info_list增加两个key，start_time和count
            roi_boxes = item.get('boxes')
            if roi_boxes:  # detect_info中没有该roi区域的识别信息，更新roi_info_list
                roi_info_list[index]['start_time'] = now_strptime
                roi_info_list[index]['count'] = 1  # 当alarm_time=0时，立马报警
                info_add_list.append(roi_info_list[index])
            roi_info_list[index]['ftime'] = 1  # detect_info is [], add ftime = 1
        detect_info = detect_info + info_add_list
        info_add_list = []

    if len(detect_info):
        for index, item in enumerate(roi_info_list):  # 循环当前识别到roi信息
            name = item.get('roi_name')
            boxes = item.get('boxes')  # 二维
            cls = item.get('cls')
            info_name_list = []
            for j, info in enumerate(detect_info):
                info_name = info.get('roi_name')
                info_name_list.append(info_name)
            if name in info_name_list:
                for i, info in enumerate(detect_info):
                    info_name = info.get('roi_name')
                    ftime = info.get('ftime')
                    t = int(ftime * rate)
                    if name == info_name:  # 如果在detect_info中已经有当前roi的信息
                        count = info.get('count')
                        start_time = info.get('start_time')
                        inter_time = int(now_strptime - start_time)
                        if inter_time >= alarm_time:  # 如果大于规定的告警时间, 以秒结算，如果以分钟，则*60
                            if count >= t and inter_time <= (alarm_time + wait_time):  # 以秒结算，如果以分钟，则*60
                                out_boxes.extend(boxes)
                                face_result.extend(cls)
                                timeArray = time.localtime(int(start_time))
                                start_time_array = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                timeArray = time.localtime(int(now_strptime))
                                end_time_array = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                end_time_array = end_time_array.split(' ')[1]
                                if alarm_time and aiot_set:
                                    if name:
                                        if alarm_info:
                                            alarm_info = alarm_info + f'|{name}'
                                        else:
                                            alarm_info = alarm_info + f'在{dev_name}{name}'
                                            alarm_ftime_info = alarm_ftime_info + f' {start_time_array}-{end_time_array}时间段内检测到{behavior_info}'

                                        if not alarm_info_dict.get('info_rois'):
                                            alarm_info_dict['info_rois'] = f'{name}'
                                        else:
                                            alarm_info_dict['info_rois'] += f'|{name}'
                                    else:  # 针对没有roi的摄像头
                                        alarm_info = alarm_info + f'在{dev_name}'
                                        alarm_ftime_info = alarm_ftime_info + f' {start_time_array}-{end_time_array}时间段内检测到{behavior_info}'

                                    alarm_info_dict['info_ftime'] = f' {start_time_array}-{end_time_array}时间段内'
                                else:
                                    if name:
                                        if alarm_info:
                                            alarm_info = alarm_info + f'|{name}'
                                        else:
                                            alarm_info = alarm_info + f'在{dev_name}{name}'
                                            alarm_ftime_info = alarm_ftime_info + f'检测到{behavior_info}'

                                        if not alarm_info_dict.get('info_rois'):
                                            alarm_info_dict['info_rois'] = f'{name}'
                                        else:
                                            alarm_info_dict['info_rois'] += f'|{name}'
                                    else:
                                        alarm_info = alarm_info + f'在{dev_name}'
                                        alarm_ftime_info = alarm_ftime_info + f'检测到{behavior_info}'

                                roi_info_result = {k: v for k, v in roi_info_list[index].items() if k not in ['start_time', 'count', 'ftime']}
                                out_result.append(roi_info_result)  # 要保存在img_process.out_result中

                            info_del_list.append(info)  # 超过设置的时间，删除info
                        else:  # 小于alarm_time分钟且boxes不为空则增加计数
                            if len(boxes) > 0:
                                count += 1
                                detect_info[i]['count'] = count
                        break
            else:  # detect_info中没有该roi区域的识别信息，更新roi_info_list
                roi_boxes = item.get('boxes')
                if roi_boxes:  # 有bbox，增加start_time、count
                    roi_info_list[index]['start_time'] = now_strptime
                    roi_info_list[index]['count'] = 1
                    info_add_list.append(roi_info_list[index])

    if str(behavior_number) == '5000001':
        if face_info and alarm_time:
            face_diff = list(set(face_result) - set(face_info))
            face_inter = set(face_result).intersection(set(face_info))
            if face_diff and face_inter:
                alarm_sub_info = alarm_ftime_info.split('检')[0]
                alarm_face_info = '、'.join(face_diff)
                alarm_ftime_info = alarm_sub_info + alarm_face_info + '替换了驾驶员' + '、'.join(face_info)
                face_info = face_diff
            else:
                out_boxes = []
                out_result = []
        else:
            face_info = face_result
            alarm_sub_info = alarm_ftime_info.split('检')[0]
            alarm_face_info = '、'.join(face_info)
            alarm_ftime_info = alarm_sub_info + alarm_face_info + '驾驶员通过了人脸认证'

    for info in info_del_list:
        detect_info.remove(info)

    detect_info = detect_info + info_add_list
    for index, info in enumerate(detect_info):
        if info.get('ftime'):
            detect_info[index]['ftime'] = info.get('ftime') + 1
        else:
            detect_info[index]['ftime'] = 1

    if not out_result:
        alarm_info_dict = {}

    img_process.out_boxes = out_boxes  # 用于人数统计
    img_process.out_result = out_result  # 用于告警展示
    img_process.alarm_info = alarm_info + alarm_ftime_info
    img_process.alarm_info_dict = alarm_info_dict
    img_process.dev_params['dev_rules']['behavior_' + str(behavior_number)]['detect_info'] = detect_info
    img_process.dev_params['dev_rules']['behavior_' + str(behavior_number)]['face_info'] = face_info


@register
def transform_info(**kwargs):
    """统一数据输出格式-针对无roi的算法场景"""
    out_boxes_list = kwargs.get('img_process').boxes
    behavior_info = kwargs.get('dev_rules').get('behavior_info')

    out_result = dict()
    alarm_info = f'检测到{behavior_info}'

    out_result['boxes'] = out_boxes_list
    out_result['alarm_info'] = alarm_info
    return out_result


@register
def transform_roi_info(**kwargs):
    """统一数据输出格式-针对结合roi的算法场景"""
    roi_info_list = kwargs.get('roi_info_list')
    behavior_info = kwargs.get('dev_rules').get('behavior_info')

    out_result = dict()
    out_boxes = []
    alarm_info = ''
    for index, info in enumerate(roi_info_list):
        info_name = info.get('name')
        boxes = info.get('boxes')
        alarm_info = alarm_info + f'在{info_name}检测到{behavior_info} '
        out_boxes.extend(boxes)

    out_result['boxes'] = out_boxes
    out_result['alarm_info'] = alarm_info
    return out_result


@register
def transform_result(img_process):
    """构造result"""
    kwargs = img_process.dev_params  # attr
    if img_process.out_result:
        img_process.behavior_result['alarm_face'] = kwargs.get('alarm_face')
        img_process.behavior_result['behavior_number'] = kwargs.get('behavior_number')
        img_process.behavior_result['result'] = img_process.out_result
        img_process.behavior_result['alarm_info'] = img_process.alarm_info
        img_process.behavior_result['alarm_info_dict'] = img_process.alarm_info_dict
