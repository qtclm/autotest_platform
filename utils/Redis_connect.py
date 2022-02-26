import sys
sys.path.append('../')
from utils.Redis_public import OperationRedis
from utils.OperationDatas import OperationYaml

class Config(object):
    def __init__(self):
        config=OperationYaml().read_data()
        self.dataBaseConfig=config['config']

class Redis_qa(OperationRedis,Config):
    def __init__(self):
        Config.__init__(self)
        tencent_cloud_redis=self.dataBaseConfig['redis_conf']
        tencent_cloud_redis['db'] = 0
        super().__init__(**tencent_cloud_redis)



if __name__=="__main__":
    # re=Redis_tencentcloud()
    # print(re.hash_getvalues('py'))
    pass

