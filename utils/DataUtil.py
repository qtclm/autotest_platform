# -*- coding: utf-8 -*-
"""    
__author__ = qtclm
File Name：     DataUtil
date：          2020/8/12 16:10 
"""
import re
import traceback

from utils.Operation_logging import logs
from jsonpath_rw_ext import parse
from utils.timeUtil import timeUtil
from utils.customException import *


class dataUtil(timeUtil):
    def __init__(self):
        self.log = logs()

    # 返回依赖数据
    def depend_data_parse(self,dependkey,response_data,index='one'):
        __dict={}#存放字典
        '''处理依赖'''
        if dependkey:
            # 匹配字典key
            depend_data_index = dependkey.rfind('.')
            depend_data_str = dependkey[depend_data_index + 1:]
            try:
                math_value = self.json_path_parse_public(json_path=dependkey,json_obj=response_data)
                if math_value:
                    if index=='one':
                        math_value=math_value[0]
                    __dict[depend_data_str]=math_value
                    return __dict
                else:
                    return None
            except IndexError as indexerror:
                return None
        else:
            return None

    # 根据jsonpath表达式获取json对象公共方法,部分功能还需要测试
    def json_path_parse_public(self,json_path,json_obj,get_index:bool=False):
        if json_path:
            # 定义要获取的key
            # 定义响应数据,key从响应数据里获取
            # print(madle)
            # math.value返回的是一个list，可以使用索引访问特定的值jsonpath_rw的作用就相当于从json里面提取响应的字段值
            try:
                json_exe = parse(json_path)
                madle = json_exe.find(json_obj)
                math_value = [i.value for i in madle]
                if get_index:
                    return math_value[0]#返回匹配结果第0个元素

                return math_value
            except IndexError as indexerror:
                # print(indexerror)
                traceback.print_exc()
                return []
            except Exception as e:
                # print(e)
                traceback.print_exc()
                raise jsonPathExtractError(Reason="jsonpath表达式：{}，提取对象{}".format(json_path,json_obj))

        else:
            return []





if __name__ == "__main__":
    du=dataUtil()
    # du.json_path_parse_public(json_obj={"1":"2"},json_path="$.*")
    s1=du.json_path_parse_public(json_obj={'cmd': None, 'code': '2000000000', 'data': {'auditedAmount': 21.6928, 'costs': [{'auditedAmount': 10.0, 'billedAmount': 10.0, 'adjustReason': '', 'type': '配送费/配送费1', 'audited': True, 'planAmount': 10.0, 'pictures': []}, {'auditedAmount': 11.6928, 'billedAmount': 11.6928, 'adjustReason': '', 'type': '配送费/配送费2', 'audited': True, 'planAmount': 0, 'pictures': []}], 'shippingOrderCode': 'F211016007006000022', 'oilCardPayType': 1, 'oilCardFee': 0.0, 'payAuditId': 38770, 'stepPayAmounts': [21.69], 'billCode': 'PB211020007006000011', 'billedAmount': 21.6928, 'createTime': 1634732948753, 'adjustedAmount': 0, 'orders': [{'loadWeight': 10.0, 'transportWeight': 10.0, 'startLoadWeight': 10.0, 'auditSign': '10.0000kg0.0010方10.0000件', 'startTransportTime': 1634375010000, 'lcensePlate': '沪ES3016', 'loadNumber': 10.0, 'goodsValue': '10.00000', 'plateNumber': '沪ES3016', 'signingTime': 1634375027000, 'dispatchTime': 1634374977440, 'tenantName': '安徽璞润贸易有限责任公司', 'loadVolums': 0.001, 'transportNumber': 10.0, 'waybillCode': 'Y211016007006000052', 'driverName': '浦发2894885449', 'driverPhone': '18883612487', 'startLoadNumber': 10.0, 'auditLoad': '10.0000kg0.0010方10.0000件', 'startLoadVolume': 0.001, 'transportVolume': 0.001}], 'id': 8211, 'auditorName': '秦敏'}, 'httpCode': 200, 'msg': None, 'ticket': None, 'version': None}
,json_path="$.data.costs[*].auditedAmount")
    print(s1)
    # print(du.time_to_str_ajdust(num=-30))
    # print(du.str_to_time_adjust(num=-30))
    # print(du.adjust_time(num=-30))
