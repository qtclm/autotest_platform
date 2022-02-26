import hashlib
import re
from urllib.parse import urljoin,urlparse,urlunparse
from posixpath import normpath

class otherUtil(object):
    # 输入字符串，输出字符串的大小写与首字母大写以及字符串本身
    def strOutputCase(self, str_in):
        if isinstance(str_in, str):
            str_in = str_in
        else:
            str_in = str(str_in)
        out_str_tuple = (str_in, str_in.lower(), str_in.upper(), str_in.capitalize())
        return out_str_tuple

    # '''将带有time关键字的参数放到字符串末尾'''
    def standardStr(self, str_in, kw_str='time', kw_str2='sign'):
        spilt_sign = '\n'
        split_list = str_in.split(spilt_sign)
        # print(self.log.out_varname(split_list))
        str_out = ''
        # '''获取参数中带有time、sign得参数'''
        __time = [i for i in split_list if kw_str in i]
        __sign = [i for i in split_list if kw_str2 in i]
        # '''过滤参数中带有time得参数'''
        __nottime = [i for i in split_list if not i in __time or __sign]
        # '''如果list个数大于等于2，代表至少有两个请求参数，直接正常拼接字符串'''
        if len(__nottime) >= 2:
            str_out = spilt_sign.join(__nottime)
        # '''如果list个数为0，代表至少过滤后没有请求参数，这时候手动将time参数赋值给list，防止处理出错,直接使用空字符串拼接'''
        elif len(__nottime) == 0:
            __nottime.extend(__time)
            # '''判断__time的个数'''
            if len(__time) == 1:
                str_out = ''.join(__nottime)
            elif len(__time) == 0:
                print("参数都没有，还处理个球嘛")
                return None
            else:
                str_out = spilt_sign.join(__nottime)
        # 否则代表list只有一个参数，直接使用空字符串拼接
        else:
            str_out = ''.join(__nottime)
        return str_out

    # 将str转换为dict
    def strToDict(self, str_in, space_one=':', space_two='\n'):
        # '''将str转换为dict输出'''
        # '''将带有time关键字的参数放到字符串末尾'''
        str_in = self.standardStr(str_in)
        # print(str_in)
        if str_in:
            split_list = str_in.split(space_two)
            str_in_dict = {}
            for i in split_list:
                colon_str_index = i.find(space_one)
                if colon_str_index == -1:
                    # '''处理firefox复制出来的参数'''
                    space_one = '\t' or ' '
                    colon_str_index = i.find(space_one)
                # '''去掉key、value的空格,key中的引号'''
                str_in_key = i[:colon_str_index].strip()
                if str_in_key:
                    str_in_key = str_in_key.replace('"', '')
                    str_in_key = str_in_key.replace("'", '')
                    # 正则过滤无用key,只保留key第一位为字母数据获取[]_
                    str_sign = re.search('[^a-zA-Z0-9\_\[\]+]', str_in_key[0])
                    if str_sign is None:
                        # 处理value中的空格与转义符
                        str_in_value = i[colon_str_index + 1:].strip()
                        str_in_value = str_in_value.replace('\\', '')
                        try:
                            # 遇到是object类型的数据转换一下
                            str_in_value = eval(str_in_value)
                        except BaseException as error:
                            str_in_value = str_in_value
                        str_in_dict[str_in_key] = str_in_value
            return str_in_dict
        else:
            print("参数都没有，还处理个球嘛")
            return None

    # 将dict转换为str
    def dictToStr(self, dict_in, space_one='=', space_two='&'):
        if isinstance(dict_in, dict) and dict_in:
            str_out = ''
            for k, v in dict_in.items():
                str_out += '{}{}{}{}'.format(k, space_one, v, space_two)
            if str_out[-1] == space_two:
                str_out = str_out[:-1]
            return str_out
        return None

    # 对字典进行排序
    def sortedDict(self,dict_in):
        if isinstance(dict_in, dict):
            __dict = dict(sorted(dict_in.items(), key=lambda x: x[0]))  # 对字典进行排序
            return __dict
        else:
            return None

    # ''' 一个用于指定输出的postman的方法，去除空格'''
    def requestDataTostr_postman(self, str_in, space_one=':', space_two='\n'):
        str_dict = self.strToDict(str_in)
        str_out = self.dictToStr(str_dict, space_one=space_one, space_two=space_two)
        return str_out


    # '''生成md5加密字符串'''
    def md5_Encry(self, str_in,upper=None):
        str_out = hashlib.md5()  # 采用md5加密
        str_out.update(str(str_in).encode(encoding='utf-8'))
        md5=str_out.hexdigest()
        if upper==True:
            return md5.upper()
        return  md5

    # '''生成sha1加密字符串'''
    def sha1_Encry(self, str_in):  # 对字符串进行加密
        str_out = hashlib.sha1()  # 采用sha1加密
        str_out.update(str(str_in).encode(encoding='utf-8'))
        return str_out.hexdigest()

    # '''生成sha256加密字符串'''
    def sha256_Encry(self,str_in):
        str_out = hashlib.sha256()  # 采用sha1加密
        str_out.update(str(str_in).encode(encoding='utf-8'))
        return str_out.hexdigest()



    # 针对url进行拼接
    def url_join(self,base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    # 生成文件行字符串，传入数组，分割符，完成字符串组装
    def generate_fileLineStr(self,*args,join_str='\t'):
        generate_str=''
        for i in args:
            generate_str+=str(i)+str(join_str)
        return generate_str.strip()


    # 将断言中的true/false/null，转换为python对象
    def assertToPyobject(self, str_in):
        str_dict = self.strToDict(str_in)
        for k in str_dict:
            if str_dict[k] == 'true':
                str_dict[k] = True
            elif str_dict[k]== 'flase':
                str_dict[k] = False
            elif str_dict[k] == 'null':
                str_dict[k] = None
        return str_dict

    # 将json_str中的true/false/null，转换为python对象
    def jsonStrToPyobject(self,str_in):
        str_in = str(str_in).replace('true', 'True').replace('false', 'False').replace('null', 'None')\
            .replace('<NULL>', 'None')
        try:
            json_pyobj=eval(str_in)
            return json_pyobj
        except BaseException as e:
            # print('字符串处理失败，原因:{}'.format(e))
            return str_in

    # 将字符串转换为有效得python对象
    def strToPyobject(self,str_in):
        if str(str_in).lower()=='None'.lower():
            return None
        elif str(str_in).lower()=='False'.lower():
            return False
        elif str(str_in).lower()=='True'.lower():
            return True
        else:
            return str_in