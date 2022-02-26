import sys
sys.path.append('../')
from utils.Mysql_public import Mysql_operation
from utils.OperationDatas import OperationYaml
import pymysql

class Config(object):
    def __init__(self,env='qa'):
        if not env in('qa','dev'):
            raise Exception("不支持的环境配置")
        config=OperationYaml().read_data()
        self.dataBaseConfig=config['config'][env]

class Mysql_qa(Mysql_operation,Config):
    def __init__(self):
        Config.__init__(self)
        tencent_cloud_mysql_conf=self.dataBaseConfig['mysql_conf']
        tencent_cloud_mysql_conf['db'] = 'hope_saas_bms'
        tencent_cloud_mysql_conf["cursorclass"]=pymysql.cursors.DictCursor
        print(tencent_cloud_mysql_conf)
        super().__init__(**tencent_cloud_mysql_conf)


class Mysql_prod(Mysql_operation,Config):
    def __init__(self):
        Config.__init__(self)
        tencent_cloud_mysql_conf=self.dataBaseConfig['mysql_conf_prod']
        tencent_cloud_mysql_conf['db'] = 'hope_saas_oms'
        tencent_cloud_mysql_conf["cursorclass"]=pymysql.cursors.DictCursor
        super().__init__(**tencent_cloud_mysql_conf)

if __name__=="__main__":
    pd=Mysql_qa()
    # list2=[]
    # for i in range(10):
    #     list_str='("'+'","'.join(list2[900*(i):900*(i+1)])+'")'
    #     sql_info=pd.sql_operation(sql_operation='''
    #     select contract_code,product_code,odr_no from oms_order_msg where odr_no in {}
    #     '''.format(list_str),limitOne=False)
    #     sql_info_2=[ ",".join(list(i.values())) for i in sql_info]
    #     pd.log.info("\n{}".format("\n".join(sql_info_2)))
