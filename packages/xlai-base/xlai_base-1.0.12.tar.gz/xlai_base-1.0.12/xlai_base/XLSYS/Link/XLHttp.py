# coding=utf8
import json
from typing import Dict

import requests

from ..Entities import XLDE, XLContext, XLBaseException, XLExceptionEnum
from ...Util import XLLogger
from ...Util.XLTools import request_to_curl


def doXLFuncPost(url, func_key, data_dict: Dict[str, XLDE], context: XLContext = None, env_dict: dict = None,
                 headers=None,
                 prn=True):
    logger = XLLogger()
    input_data_dict = {k: d.toLinkDE() for k, d in data_dict.items()}
    data = {'func_key': func_key,
            'data_dict': input_data_dict,
            'env_dict': env_dict
            }
    mheaders = {'http_debug': '1'}
    if headers is not None:
        mheaders.update(headers)
    response = requests.post(url, json=data, headers=mheaders)
    # 打印请求日志
    if context is not None:
        extra = {"mod": "http", "context_id": context.context_id,
                 "global_info": context.global_info.to_dict()}
    else:
        extra = {"mod": "http", "context_id": "", "global_info": ""}
    logger.requestLogger.info("{}".format(request_to_curl(response.request)), extra=extra)
    if prn:
        logger.infoContext(context, '{} {} {} {}'.format('doXLFuncPost', response.status_code, response.text,
                                                         json.dumps(data, ensure_ascii=False)))
    if response.status_code == 201:
        raise XLBaseException(XLExceptionEnum.http_debug_timeout)
    if response.status_code == 200:
        backInfo = json.loads(response.text)
        return backInfo.get('code'), backInfo.get('data_dict'), backInfo.get('env_dict')
    return -1, {}, {}
    pass


def doXLEventPost(url, event, data_dict: Dict[str, XLDE], want_keys=None, context: XLContext = None,
                  env_dict: dict = None, headers=None, prn=True):
    logger = XLLogger()
    input_data_dict = {k: d.toLinkDE() for k, d in data_dict.items()}
    want_keys = [] if want_keys is None else want_keys
    data = {'event': event,
            'data_dict': input_data_dict,
            'want_keys': want_keys,
            'env_dict': env_dict}
    mheaders = {'http_debug': '1'}
    if headers is not None:
        mheaders.update(headers)
    response = requests.post(url, json=data, headers=mheaders)
    # 打印请求日志
    if context is not None:
        extra = {"mod": "http", "context_id": context.context_id,
                 "global_info": context.global_info.to_dict()}
    else:
        extra = {"mod": "http", "context_id": "", "global_info": ""}
    logger.requestLogger.info("{}".format(request_to_curl(response.request)), extra=extra)
    if prn:
        logger.infoContext(context, '{} {} {} {}'.format('doXLEventPost', response.status_code, response.text,
                                                         json.dumps(data, ensure_ascii=False)))
    if response.status_code == 201:
        raise XLBaseException(XLExceptionEnum.http_debug_timeout)
    if response.status_code == 200:
        backInfo = json.loads(response.text)
        return backInfo.get('code'), backInfo.get('data_dict'), backInfo.get('env_dict')
    return -1, {}, {}
    pass


def doXLLearnPost(url, context_id, event, data_dict: Dict[str, XLDE], context: XLContext = None,
                  env_dict: dict = None, headers=None, prn=True):
    logger = XLLogger()
    input_data_dict = {k: d.toLinkDE() for k, d in data_dict.items()}
    data = {'event': event,
            'context_id': context_id,
            'data_dict': input_data_dict,
            'env_dict': env_dict}
    mheaders = {'http_debug': '1'}
    if headers is not None:
        mheaders.update(headers)
    response = requests.post(url, json=data, headers=mheaders)
    # 打印请求日志
    if context is not None:
        extra = {"mod": "http", "context_id": context.context_id,
                 "global_info": context.global_info.to_dict()}
    else:
        extra = {"mod": "http", "context_id": "", "global_info": ""}
    logger.requestLogger.info("{}".format(request_to_curl(response.request)), extra=extra)
    if prn:
        logger.infoContext(context, '{} {} {} {}'.format('doXLLearnPost', response.status_code, response.text,
                                                         json.dumps(data, ensure_ascii=False)))
    if response.status_code == 201:
        raise XLBaseException(XLExceptionEnum.http_debug_timeout)
    if response.status_code == 200:
        backInfo = json.loads(response.text)
        return backInfo.get('code'), backInfo.get('data_dict'), backInfo.get('env_dict')
    return -1, {}, {}
    pass
