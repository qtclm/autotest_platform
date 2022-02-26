import datetime

import django
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
import apiManage.models
from Common.model_common import *


class case(models.Model):
    class Meta:
        verbose_name = _(u'用例列表')
        # 设置此字段可避免app多展示一个s
        verbose_name_plural = _(u'用例列表')
        db_table='case'

    assert_type=[
        ('contains', "文本包含"),
        ('regEx','正则表达式'),
        ('jsonPath','json解析'),
        ('sql','sql断言'),
        ('dict','字典断言'),

    ]

    case_name=models.CharField(max_length=128,blank=False,verbose_name="用例名称",unique=True) #将case作为一个唯一键
    case_desc=models.CharField(max_length=1024,blank=True,verbose_name="用例描述")
    case_api_ids=models.ForeignKey(apiManage.models.api,on_delete=models.SET_NULL,null=True,verbose_name="关联的接口集合")
    case_is_run=models.BooleanField(choices=model_common_field.bool_enum,verbose_name="用例是否执行",default=True)
    case_preposition_step=models.TextField(verbose_name="用例前置步骤",default="",blank=True)
    case_postposition_step=models.TextField(verbose_name="用例后置步骤",default="",blank=True)
    case_depend_case=models.ForeignKey('caseManage.case',verbose_name='依赖的用例',null=True,on_delete=models.SET_NULL,default="caseManage.models.case",blank=True)
    case_assert_content=models.CharField(max_length=1024,verbose_name="断言文本内容",blank=True,help_text="根据断言类型,可能使用不同的值：jsonpath/正则/sql/对象断言时，分别为jsonpath表达式/正则表达式/sql语句/dict")
    case_expect_result=models.CharField(max_length=1024,verbose_name="用例预期结果",blank=True)
    case_assert_type=models.CharField(choices=assert_type,verbose_name="断言类型",default=assert_type[0],blank=False,max_length=64)
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL, default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now, editable=False)

    def __str__(self):
        return str(self.case_name)


class caseLog(models.Model):
    class Meta:
        verbose_name = _(u'用例执行日志')
        # 设置此字段可避免app多展示一个s
        verbose_name_plural = _(u'用例执行日志')
        db_table='case_log'

    caseLog_name=models.CharField(max_length=128,verbose_name="用例日志名称",editable=False)
    caseLog_caseId=models.IntegerField(verbose_name="关联的测试用例",editable=False)
    # caseLog_caseId=models.ForeignKey(case, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=case)
    caseLog_resp=models.TextField(verbose_name="请求响应",blank=True,default="",editable=False)
    caseLog_res_status_code=models.IntegerField(verbose_name="请求响应code",editable=False,blank=True)
    caseLog_res_time=models.FloatField(verbose_name="请求响应时间",default=0.0,editable=False)
    caseLog_type=models.CharField(default="",verbose_name="用例日志类型",blank=False,help_text="'debug:用例调试日志,info:用例运行日志",max_length=32)
    # editable 不展示此字段
    caseLog_run_status=models.IntegerField(verbose_name="api最新执行状况",choices=model_common_field.bool_enum,default=False,editable=False)
    caseLog_case_is_pass=models.BooleanField(verbose_name="用例是否执行通过",default=False,editable=False)
    caseLog_last_run_lable=models.IntegerField(verbose_name="用例最新执行日志标识",default=0,help_text="只有最近一次执行的用例会将标记更新为1，其余情况下为0")
    caselog_remark=models.TextField(verbose_name="备注",blank=True)
    caseLog_report_id=models.IntegerField(verbose_name="测试日志关联的测试报告id",blank=True,null=True)
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now,editable=False)


class caseReport(models.Model):
    class Meta:
        verbose_name = _(u'测试报告')
        # 设置此字段可避免app多展示一个s
        verbose_name_plural = _(u'测试报告')
        db_table='case_report'

    caseReport_name=models.CharField(verbose_name="测试报告名称",max_length=128)
    caseReport_start_time=models.DateTimeField(verbose_name="测试报告开始执行时间",max_length=128,default=django.utils.timezone.now)
    caseReport_end_time=models.DateTimeField(verbose_name="测试报告结束执行时间",max_length=128,default=django.utils.timezone.now)
    caseReport_run_time=models.IntegerField(verbose_name="测试报告执行时间",default=0)
    case_run_num=models.FloatField(verbose_name="本次运行用例个数",default=0.0,editable=False)
    case_skip_num=models.IntegerField(verbose_name="本次跳过运行用例个数",default=0,editable=False)
    case_pass_num=models.IntegerField(verbose_name="用例通过个数",default=0,editable=False)
    case_fail_num=models.IntegerField(verbose_name="用例失败个数",default=0,editable=False)
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now,editable=False)


