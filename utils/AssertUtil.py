import json
import time
import traceback

import pymysql

from utils.DataUtil import dataUtil
from utils.customException import *
from collections.abc import Iterable
import operator
from utils.Mysql_public import Mysql_operation
from utils.Mongo_public import OperationMongo

class AssertUtil(object):
    def __init__(self):
        self.data=dataUtil()
        self.assert_result_detail=""

    # 正则表达式断言
    def regex_assert(self,regex_match_str:str,expect_result:str,obj:str) -> bool:
        import re
        # print("regex_match_str:",regex_match_str)
        out_result=re.search(regex_match_str,self.string_operation(obj))
        # print("out_result:",out_result)
        if not out_result:
            return False
        if out_result.group()!=expect_result:
            return False
        return True

    # 标准化字符串
    def string_operation(self,str_in:str):
        str_in=str(str_in).replace(' ','').replace("'",'"').replace('\n','').replace('\r','')
        return str_in

    # 字符断言
    def contasins_assert(self,expect_result:str,obj:str) -> bool:
        if isinstance(obj,dict):
            obj=json.dumps(obj,ensure_ascii=False,indent=None)
        expect_result=self.string_operation(expect_result)
        obj=self.string_operation(obj)
        print(expect_result)
        print(obj)
        if str(expect_result) in str(obj):
            return True
        return False

    # jsonpath断言
    def jsonPath_assert(self,json_path_str:str,expecet_result,obj) -> bool:
        if  not  str(json_path_str).startswith("$"):
            raise argsTypeError(Reason="{}".format(json_path_str))
        if not isinstance(obj,dict):
            try:
                obj=eval(obj)
            except Exception as e:
                traceback.print_exc()
                return False
                # Reason = "{}--转换为dict类型失败,失败原因为:\n{}".format(obj, e)
                # raise dataTransformError(Reason="{}--转换为dict类型失败,失败原因为:\n{}".format(obj,e))
        try:
            out_result=self.data.json_path_parse_public(json_path=json_path_str,json_obj=obj)
            if len(out_result)==1 and isinstance(out_result[0],(list,tuple,set,dict)):
                out_result=out_result[0]
            if len(out_result)==1 and isinstance(expecet_result,str):
                out_result=out_result[0]
            if out_result==expecet_result:
                return True
            return self.iterable_cmp(out_result,expecet_result)

        except Exception as e:
            traceback.print_exc()
        return False

    # sql断言
    def sql_assert(self,dataBaseType,sql_statement,dataBaseConnectInfo:dict,expect_result,obj,limitOne=False) -> bool:
        try:
            if dataBaseType==0:
                dataBaseConnectInfo['cursorclass']=pymysql.cursors.DictCursor
                connect_info=Mysql_operation(**dataBaseConnectInfo)
                data_result = connect_info.sql_operation(sql_operation=sql_statement, limitOne=limitOne)
            else:
                connect_info=OperationMongo(**dataBaseConnectInfo)
                if limitOne:
                    data_result = connect_info.select_all_collection(collection_name=sql_statement['collection_name'],
                                                                 search_col=sql_statement['collection_name'],skip_col=sql_statement['skip_col'],
                                                                 sort_col=sql_statement['sort_col'],limit_num=sql_statement['limit_num'])
                else:
                    data_result = connect_info.select_one_collection(collection_name=sql_statement['collection_name'],search_col=sql_statement['collection_name'])

        except Exception as e:
            reson="数据库链接信息:{}".format(dataBaseConnectInfo)
            traceback.print_exc()
            raise DatabaseError(Reason=reson)

        if not data_result:
            return False
        if limitOne==False:
            return self.iterable_cmp(data_result,[self.string_operation(i) for i in data_result])
        else:
            print(data_result)
            print(expect_result)
            return self.map_assert(data_result,expect_result)

    # 如果是可迭代对象，调用此方法预处理
    def iterable_cmp(self,a,b) -> bool:
        if isinstance(a, Iterable) and isinstance(b, Iterable):
            a.sort(),b.sort()
            return True if operator.eq(a, b) else False
        return False

    # 比较两个字典
    def map_assert(self,a,b) -> bool:
        import dictdiffer
        # a、b如果不是dict类型，序列化为dict
        if not isinstance(a,dict):
            a=json.loads(a)
        if not isinstance(b, dict):
            b = json.loads(b)
        out_result=list(dictdiffer.diff(a, b))
        if not out_result:
            return True
        else:
            self.assert_result_detail=out_result
            # print(out_result)
            return False

if __name__=="__main__":
    as1=AssertUtil()
    # print("1$.12".startswith("$"))
    # print(['123'].sort())
    # s_time=time.perf_counter()
    # print(as1.jsonPath_assert(json_path_str='$.a', expecet_result=['123','234'], obj={"a": ['234','123']}))
    # e_time=time.perf_counter()
    # expecet_result = ['123', '234']
    # expecet_result.sort()
    # print(expecet_result)
    # list_2=['234','123']
    # list_2.sort()
    # print(list_2)
    # print(expecet_result == list_2)
    # print(operator.eq(expecet_result, list_2))
    # print(e_time-s_time)
    second_dict = {
        # "template": "",
        # "template2": "",'
        # "data": {
        #     "name": "鸣人",
        #     "age": 22,
        #     "sex": "男",
        #     "title": "六代火影"
        # },  # 数据
        'data2': '12'
    }

    first_dict = {
        # "template": "11",
        # "template1": "11",
        # "data": {
        #     "name": "鸣人",
        #     "age": 22,
        #     "sex": "女",
        #     "title": "六代火影"
        # },  # 数据
        'data2':'12'
    }

    first_dict=[{"tel_phone": "18160042485", "tenant_id": "T10200668"},{"tel_phone": "18160042485", "tenant_id": "T10200668"}]
    second_dict=[{"tel_phone": "18160042485", "tenant_id": "T10200668"},{"tel_phone": "18160042485", "tenant_id": "T10200668"}]
    print(as1.map_assert(first_dict, second_dict))

