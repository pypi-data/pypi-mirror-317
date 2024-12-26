import networkx as nx
from .utils import state2box


class Matcher:
    def __init__(self):
        pass

    @classmethod
    def match(cls, state_list, measure_list):
        """
        description: 最大权值匹配
        param:
            state_list: 上一帧目标坐标
            measure_list: 当前帧目标坐标
        return:
            eg:{'state_1': 'mea_1', 'state_0': 'mea_0'}
        """
        graph = nx.Graph()
        for idx_sta, state in enumerate(state_list):
            state_node = 'state_%d' % idx_sta
            graph.add_node(state_node, bipartite=0)
            for idx_mea, measure in enumerate(measure_list):
                mea_node = 'mea_%d' % idx_mea
                graph.add_node(mea_node, bipartite=1)
                score = cls.cal_iou(state, measure)

                if score is not None:
                    graph.add_edge(state_node, mea_node, weight=score)
        match_set = nx.max_weight_matching(graph)  # 最大权值匹配
        res = dict()
        for (node_1, node_2) in match_set:
            if node_1.split('_')[0] == 'mea':
                node_1, node_2 = node_2, node_1
            res[node_1] = node_2
        return res

    @classmethod
    def cal_iou(cls, state, measure):
        """
        description:计算两个bbox之间的IOU
        param:
            state:ndarray [c_x, c_y, w, h]
            measure:ndarray [c_x, c_y, w, h]
        return:
            iou值
        """
        state = state2box(state)
        measure = state2box(measure)
        s_tl_x, s_tl_y, s_br_x, s_br_y = state[0], state[1], state[2], state[3]
        m_tl_x, m_tl_y, m_br_x, m_br_y = measure[0], measure[1], measure[2], measure[3]
        # 计算相交部分的坐标
        x_min = max(s_tl_x, m_tl_x)
        x_max = min(s_br_x, m_br_x)
        y_min = max(s_tl_y, m_tl_y)
        y_max = min(s_br_y, m_br_y)
        inter_h = max(y_max - y_min, 0)
        inter_w = max(x_max - x_min, 0)
        inter = inter_h * inter_w
        if inter == 0:
            return 0
        else:
            return inter / ((s_br_x - s_tl_x) * (s_br_y - s_tl_y) + (m_br_x - m_tl_x) * (m_br_y - m_tl_y) - inter)

