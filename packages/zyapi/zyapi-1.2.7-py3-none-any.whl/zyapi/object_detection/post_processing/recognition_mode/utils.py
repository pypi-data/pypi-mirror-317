import numpy as np


def box2meas(box):
    center_x = (box[0] + box[2]) / 2
    center_y = (box[1] + box[3]) / 2
    w = box[2] - box[0]
    h = box[3] - box[1]
    return np.array([[center_x, center_y, w, h]]).T


def state2box(state):
    center_x = state[0]
    center_y = state[1]
    w = state[2]
    h = state[3]
    return [int(i) for i in [center_x - w/2, center_y - h/2, center_x + w/2, center_y + h/2]]
