import os
import re
from lxml import etree
from time import time


def get_min_bounds_index(target: tuple = (0, 0), bounds_list: list = []) -> int:
        """
        查找包含目标点的最小边界的索引。
        参数：
            target (tuple): 目标点格式为 (x, y)。
            bounds_list (list): 边界列表，格式为 [[x0, y0, x1, y1], ...]。
        返回值：
            int: 包含目标点的最小边界的索引。
        """
        min_area = float('inf')
        min_index = 0

        for i, bounds in enumerate(bounds_list):
            x0, y0, x1, y1 = bounds
            if x0 < target[0] < x1 and y0 < target[1] < y1:
                area = (x1 - x0) * (y1 - y0)
                if area < min_area:
                    min_area = area
                    min_index = i
        return min_index

def convert_position(event_xy: tuple = (0, 0), page_wh: tuple = (0, 0), device_max_xy: tuple = (0, 0)) -> tuple:
    '''
    将事件的x,y坐标转换为window_dump.xml中的坐标。
    '''
    return int(event_xy[0] * page_wh[0] / device_max_xy[0]), int(event_xy[1] * page_wh[1] / device_max_xy[1])



