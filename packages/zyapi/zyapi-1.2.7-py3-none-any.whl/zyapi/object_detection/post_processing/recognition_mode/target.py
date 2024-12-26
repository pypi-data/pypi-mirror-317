from .matcher import Matcher


class TargetRadius:
    def __init__(self, B, C, iou_threshold, pix_threshold):
        self.B = B
        self.C = C
        self.iou_threshold = iou_threshold
        self.pix_threshold = pix_threshold
        
    def init(self, bbox=None, cls=None):
        if bbox is not None:
            self.B = bbox
            self.C = cls

    @staticmethod
    def association(target_list, mea_list, cls_list):
        """
        description: 多目标关联，使用最大权重匹配
        param:
            target_list: 对象列表存着所有TargetRadius对象，已经完成init
            mea_list: 当前帧对应对象列表存着所有TargetRadius对象的目标框
        return:
            unmatch_list：未匹配的目标，新的目标或者步伐太大丢失的目标
            static_list：静止不动的目标
            del_list：丢失的目标
        """
        state_rec = {i for i in range(len(target_list))}
        mea_rec = {i for i in range(len(mea_list))}
        state_list = list()

        for target in target_list:
            state = target.B
            state_list.append(state)

        # 最大权值匹配
        match_dict = Matcher.match(state_list, mea_list)

        state_used = set()
        mea_used = set()
        match_list = list()
        unmatch_list = list()
        static_list = list()
        del_list = list()
        for state, mea in match_dict.items():
            state_index = int(state.split('_')[1])
            mea_index = int(mea.split('_')[1])
            mea_used.add(mea_index)
            state_used.add(state_index)
            match_list.append([state_list[state_index], mea_list[mea_index]])

            # 通过匹配上的bbox判断是否是静止目标
            status = target_list[state_index].update(mea_list[mea_index], cls_list[mea_index], mea_index)
            if not status:
                static_list.append(mea_index)

        for mea_new in list(mea_rec - mea_used):
            unmatch_list.append(mea_new)

        if len(state_rec) > len(mea_rec):
            for del_state in list(state_rec - state_used):
                del_list.append(del_state)

        return unmatch_list, static_list, del_list

    def update(self, mea=None, cls=None, index=None):
        """
        description: 判断是否是静止物体
        param:
            mea: 目标坐标
            cls: 目标类别
            cls: 目标索引
        return:
            True or False
        """
        status = True
        if mea is not None:
            iou = Matcher.cal_iou(self.B, mea)
            if iou > self.iou_threshold and abs(self.B[0] - mea[0]) < self.pix_threshold and abs(self.B[1] - mea[1]) < self.pix_threshold:
                status = False
            else:
                status = True

        self.init(mea, cls)
        return status
