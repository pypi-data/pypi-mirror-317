# coding=utf8
from typing import Dict, Union

from pydantic import BaseModel

from ..Entities import XLLinkDE


class HttpFuncReq(BaseModel):
    func_key: str
    data_dict: Dict[str, XLLinkDE]
    env_dict: dict = {}
    pass


class HttpEventReq(BaseModel):
    event: str
    data_dict: Dict[str, XLLinkDE]
    want_keys: Union[list] = []
    env_dict: dict = {}
    pass


class HttpLearnReq(BaseModel):
    context_id: str
    event: str
    data_dict: Dict[str, XLLinkDE]
    env_dict: dict = {}
    pass


class XLResponse(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.data_dict = {}
        self.data_dict_json = {}
        self.env_dict = {}

    def set_covert_data_dict(self, data_dict: dict):
        data_dict_json = {k: d.toLinkDE() for k, d in data_dict.items()}
        self.data_dict = data_dict
        self.data_dict_json = data_dict_json
        return self

    def to_app_back(self) -> dict:
        return {
            'code': self.code,
            'message': self.message,
            'env_dict': self.env_dict,
            'data_dict': self.data_dict_json
        }

    pass
