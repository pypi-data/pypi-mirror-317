# coding=utf8
import traceback
from enum import Enum


class XLExceptionEnum(Enum):
    http_debug_timeout = "http_debug_timeout"

    pass


class XLBaseException(Exception):
    def __init__(self, event: XLExceptionEnum, des="", **kwargs):
        self.event = event
        self.stack = traceback.extract_stack()
        self.kwargs = kwargs
        self.des = des
        self.info_dict = {}
        self.data_dict = {}
        pass

    def printStack(self):
        traceback.print_list(self.stack)
        pass

    def updateEXDataList(self, data_list: list):
        for d in data_list:
            self.data_dict[d.key] = d
        return self
        pass

    def addInfoList(self, info_dict: dict):
        self.info_dict.update(info_dict)
        return self
        pass


pass
