# coding: utf-8
import os
import socket
from .config import DBSCAN_EUCLIDEAN_EPS, SHARPNESS_LAPLACE, SHARPNESS_SMD2, OCCLUSION_THRESHOLD


class Parameter(object):
    def __init__(self):
        # ==========================image parametar ===========================#
        self.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.picture_format = '.jpg'
        self.model_zoo_dir = 'ai_detection/models/serving_origin_models'

        self.n_GPUs = 1  # if n_GPU >0, means we use GPU, if n_GPU = 0, means we use CPU
        self.ResultImageDir = 'ai_detection/results'

        # ========================== sharpness filter =======================#
        laplace_threshold, smd2_threshold = float(SHARPNESS_LAPLACE), float(SHARPNESS_SMD2)
        self.sharpness_threshold = [0.985, 40.0, smd2_threshold, laplace_threshold]

        # ========================== occlusion =======================#
        self.occlusion_threshold = float(OCCLUSION_THRESHOLD)

        # ========================== clustering model parameters ==========================#
        self.cluster_model = 'dbscan'  # 'mean_shift' or 'dbscan'
        self.cluster_mean_shift_bandwidth = 0.7

        self.cluster_dbscn_eps = float(DBSCAN_EUCLIDEAN_EPS)  # 0.9 for 'euclidean' metric is best from our experiments
        self.cluster_dbscn_min_samples = 1
        self.cluster_dbscn_metric = 'euclidean'  # 'cosine_distance' or 'euclidean'
        self.min_cluster_samples = 1  # cluster with number of samples smaller than this number will be ignored

        # ========================== tracking =======================#
        self.feature_compress_threshold = 0  # 0 if do not compress, recommend a number smaller than 0.1
        self.num_changes_to_update = 10  # we will update models, if number of picture changed is more than this num.

        self.feature_dim = 512
        self.is_feature_normed = False
        self.feature_min_len = 11

        self.similar_group_threshold = 0.5
        self.recommend_method = 'verification'  # 'clustering' or 'verification'

        # ========================= identification model parameters =========================
        self.identi_model = None  # None if use Neighbors, or 'SVM'
        self.identi_svm_kernel = 'linear'  # 'linear' or 'rbf'
        self.identi_svm_compress_threshold = 0.05

        # ========================= show sub-module running time =========================
        self.open_deblur = False

        # ========================= result thread and min_bbox thread =========================#

        self.result_thread = [0.1, 0.2, 0, 3, 0, 4]
        self.min_bbox_thread = [50, 70, 20, 90]

        # ========================================极速/优化模式=======================================
        self.iou_threshold = 0.7  # iou阈值, 用来判断是否是静止目标
        self.pix_iou_threshold = 50  # 距离阈值, 协助判断是否是静止目标, 单位为pix
        self.move_threshold = 30  # 当优化模式选择MoveDetect时的移动阈值

        # =======================================image super resolution(image_sr)=======================================

        self.rgb_range = 255
        self.sr_model_version = 150

        # ========================= variables for local test =========================
        self.show_sub_module_time = True  # used for debug
        self.local_debug_mode = False
        self.host_name = socket.gethostname()
        self.filter_angle_dir = ''
        self.filter_occlusion_dir = ''
        self.filter_uncertain_dir = ''
        self.filter_non_frontal_dir = ''
        self.filter_smd2_dir = ''
        self.filter_keypoints_dir = ''
        self.anti_spoof_dir = ''
        self.filter_reverse_dir = ''
        self.test_img_dir = 'ai_detection/test_img'
        if self.host_name != 'amax':
            self.local_debug_mode = False

        # ============================image push statistics ===============================
        self.count = 3  # 同一个摄像头下, 只识别到一个目标, 如果连续self.count帧都是一个目标且类别相同, 则进行推送

        # ============================= 跨线检测 =================================
        self.k = 1  # 有效区域的比例, 范围[0~正无穷], 如果摄像头离目标较远, 该值取大些[1~5], 其他情况取1即可
        self.interval = 5  # 需要追踪的帧数
        self.direction = True  # True or False, True为从直线的y轴正方向走到y轴负方向才算跨线, False为从直线的y轴负方向走到y轴正方向才算跨线
        self.arrow_boxes = 200  # 箭头方向的长度

        # ============================= rfb nms iou_thres =================================
        self.iou_thres_register_person = 0.6

        # ============================= person gather ====================================
        self.person_score = 0.6  # 人员阈值, 大于该阈值才进行人员聚集识别
        self.n_thr = 3  # 人员聚集人数设定

        # ============================== falldown detection ==============================
        self.slope = 0.5  # 人员脚踝和豚骨相对于水平地面的倾斜程度, 小于该斜率则认为跌倒

        # ============================== 有人无人识别模型阈值 ===============================
        self.person_threshold = 0.7

        self.debug = {
            'behavior_number': 1002012,
            'result': [{
                'roi_name': '区域1',
                'roi': [[0, 0], [0, 108], [100, 108], [192, 0]],
                'boxes': [[[0, 0], [0, 108], [100, 108], [192, 0]]]}],
            "alarm_face": [{'name': 'test', 'bbox': [112, 66, 446, 553]}],
            'alarm_info': 'debug mode',
            'alarm_info_dict': {'info_name': 'debug', 'info_rois': '', 'info_ftime': '', 'info_type': 'mode'},
            'amount': 1
        }


HYPER_PARA = Parameter()
