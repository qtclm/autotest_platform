import datetime
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _
import projectManage.models
from Common.model_common import *
import django

class environment(models.Model):
    class Meta:
        verbose_name=_(u'环境列表')
        verbose_name_plural =_(u'环境列表')
        db_table='environment'

    environment_name=models.CharField(max_length=32,blank=False,verbose_name='环境名称')
    environment_desc=models.CharField(max_length=1024,blank=True,verbose_name='环境描述')
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now)

    def __str__(self):
        return str(self.environment_name)

class haeder(models.Model):
    class Meta:
        verbose_name=_(u'请求header')
        verbose_name_plural =_(u'请求header列表')
        db_table='header'

    headers_form_urlencoded = {"Content-Type": "application/x-www-form-urlencoded"}  # 请求格式为字符串时使用crm，fwh普通请求均可使用
    headers_json = {"Content-Type": "application/json"}  # 请求数据为json格式时使用
    headers_form_data = {"Content-Type": "multipart/form-data"}  # 请求数据为表单，不带参数
    headers_form_data_boundary = {}  # 请求数据为文件上传且有附加参数得情况，headers直接传空字典
    headers_text = {"Content-Type": "text/html"}  # 服务号微信端上传图片（头像）
    headers_xml = {"x-requested-with": "XMLHttpRequest"}

        # 信息头
    header_choices=[(str(headers_form_urlencoded),str(headers_form_urlencoded)),
                    (str(headers_json),str(headers_json)),(str(headers_form_data),str(headers_form_data)),
                    (str(headers_form_data_boundary),str(headers_form_data_boundary)),
                    (str(headers_text),str(headers_text)),(str(headers_xml),str(headers_xml)),]


    header_name=models.CharField(max_length=32,blank=False,verbose_name='请求头名称')
    header_data=models.CharField(choices=header_choices,max_length=2048,default=header_choices[0])
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now,editable=False)

    def __str__(self):
        return str(self.header_name)+'_'+str(self.header_data)

class domain(models.Model):
    class Meta:
        verbose_name=_(u'域名列表')
        verbose_name_plural =_(u'域名列表')
        db_table='domain'

    domain_name=models.CharField(max_length=1024,verbose_name='域名名称')
    domain_environment=models.ForeignKey(environment,null=True,on_delete=models.SET_NULL,verbose_name='域名关联的环境id',default=environment)
    domain_project=models.ForeignKey('projectManage.project',verbose_name='域名关联的项目',null=True,on_delete=models.SET_NULL,default='projectManage.models.project')
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL, default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now, editable=False)

    def __str__(self):
        return str(self.domain_project)+'_'+str(self.domain_environment)+'_'+str(self.domain_name)

class api(models.Model):


    class Meta:
        verbose_name = _(u'接口列表')
        # 设置此字段可避免app多展示一个s
        verbose_name_plural = _(u'接口列表')
        db_table='api'

    req_method=[
        ("GET",'GET'),
        ("POST", 'POST'),
        ("PUT", 'PUT'),
        ("DELETE", 'DELETE'),
    ]


    api_name=models.CharField(verbose_name="接口名称",max_length=128,blank=True)
    api_req_method=models.CharField(verbose_name="请求方式",max_length=128,blank=False,choices=req_method,default=req_method[0])
    api_domain=models.ForeignKey(domain,verbose_name="请求域名",on_delete=models.SET_NULL,null=True,default=domain)
    api_version=models.ForeignKey('projectManage.version', verbose_name=_('项目关联的版本信息'), null=True, on_delete=models.SET_NULL)
    api_url=models.CharField(verbose_name="请求url",max_length=1024,blank=False)
    api_header=models.ForeignKey(haeder,verbose_name="请求header",null=True,on_delete=models.SET_NULL,default=haeder)
    api_request_data=models.TextField(verbose_name="请求参数",default=None,blank=True,null=True)


    def __str__(self):
        return str(self.api_name)