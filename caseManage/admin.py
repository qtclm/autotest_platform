import datetime
import json
import logging
import os
import time
import traceback

from django.db.models import Count, Max, Min, Q
from django.utils.safestring import mark_safe

from Common.model_common import get_model_dict
from Common.modelAdmin_common import commonAdmin,readOnlyAdmin
from django.contrib import admin
# Register your models here.
from apiManage.models import domain
from caseManage.models import case, caseLog,caseReport
from django.contrib import messages
from utils.Runmethod import RunMethod
from apiManage.models import api
from utils.timeUtil import *
from utils.customException import *
from utils.AssertUtil import AssertUtil


logger = logging.getLogger(__name__)
timeUtil=timeUtil()
assertUtil=AssertUtil()
case_report_path = 'testReport/'
if not os.path.exists(case_report_path):
    os.makedirs(case_report_path)

# 写入测试日志
def write_caseLog(reqeust,obj:case,log_type:str,case_is_pass,resp,res:RunMethod):
    case_log = caseLog()
    case_log.__dict__.update(obj.__dict__)
    case_log.id=caseLog.objects.count()+1
    case_log.caseLog_name=obj.case_name+"_的运行日志,执行时间为："+str(timeUtil.timestamp_toString(timeUtil.get_timestamp()))
    log_type = log_type if log_type in ('debug', 'info') else "debug"
    case_log.caseLog_type = log_type
    case_log.caseLog_resp = json.dumps(resp)
    case_log.caseLog_res_time = res.res_time
    case_log.caseLog_res_status_code = res.res_status_code
    case_log.caseLog_caseId = obj.id
    caseLog.creator=reqeust.user
    case_log.created_date=datetime.datetime.now()
    case_log.caseLog_last_run_lable=1
    case_log.caseLog_case_is_pass=case_is_pass

    if int(res.res_status_code)>=400:
        case_log.caseLog_run_status=0
        caseLog.caselog_remark='网络请求失败'
    else:
        case_log.caseLog_run_status = 1

    case_log.save() #更新

def executeRequest(modeladmin, request, queryset):
    '''执行接口请求调试'''
    res = RunMethod()
    for obj in queryset:
        cases = case()
        cases.__dict__.update(obj.__dict__)
        # 注意这里需要使用模型来调用
        # case_obj_list=case.objects.filter(case_name=obj) #filter:返回一个queryset对象
        case_obj=case.objects.get(case_name=obj) #返回唯一对象，如果有多个对象，将触发异常 get() returned more than one case -- it returned n（n为对象数量）!
        # 获取用例关联的接口信息
        case_api_ids_obj=case_obj.case_api_ids
        api_domin_name=case_api_ids_obj.api_domain.domain_name
        apiUrl = api_domin_name + case_api_ids_obj.api_url
        api_method=case_api_ids_obj.api_req_method
        api_data=case_api_ids_obj.api_request_data
        api_header=case_api_ids_obj.api_header
        result = res.run_main(url=apiUrl,method=api_method,data=api_data,headers=api_header.header_data)
        case_run_status=assert_public(assert_type=case_obj.case_assert_type,assert_content=case_obj.case_assert_content,
                                      expect_result=case_obj.case_expect_result,resp=result)
        # print("case_run_status:",case_run_status)
        '''写入用例日志'''
        write_caseLog(reqeust=request,obj=case_obj,log_type='debug',resp=result,res=res,case_is_pass=str(case_run_status))
    messages.add_message(request, messages.INFO, '执行完毕')  # 在页面上展示的消息

# 写入测试报告
def write_testCaseReport(request,start_time):
    case_report=caseReport()
    case_report.caseReport_start_time=start_time
    report_time=str(timeUtil.timestamp_toString(
        timeUtil.get_timestamp()))
    case_report.caseReport_name="测试报告--"+report_time
    case_report.caseReport_url= case_report_path +report_time
    case_report.case_run_num=case.objects.filter(case_is_run=1).count()
    case_report.case_skip_num=case.objects.filter(case_is_run=0).count()
    case_report.creator=request.user
    # distinct:在mysql中不能直接指定字段去重，需要使用values，然后在去重
    # case_report.case_pass_num=caseLog.objects.filter(caseLog_run_status=1).values('caseLog_caseId').distinct().count()
    case_report.case_pass_num=caseLog.objects.filter(Q(caseLog_run_status=1) & Q(caseLog_type='info') & Q(caseLog_last_run_lable=1)).count()
    case_report.case_fail_num=caseLog.objects.filter(Q(caseLog_run_status=0) & Q(caseLog_type='info') & Q(caseLog_last_run_lable=1)).count()
    case_report.caseReport_end_time=datetime.datetime.now().replace(microsecond=0)
    # case_report.caseReport_run_time="2.2%f"%(timeUtil.string_toTimestamp(timeUtil.datetime_toString(case_report.caseReport_end_time))-
    #                             timeUtil.string_toTimestamp(timeUtil.datetime_toString(case_report.caseReport_start_time)))
    
    case_report.save()

# 根据断言类型进行断言
def assert_public(assert_type,assert_content,expect_result,resp)->bool:
    if assert_type in ("",None):
        print("断言类型为空，默认执行通过")
        return True
    elif assert_type=="contains":
        return assertUtil.contasins_assert(expect_result=expect_result,obj=resp)
    elif assert_type=='regEx':
        return assertUtil.regex_assert(regex_match_str=assert_content,expect_result=expect_result,obj=resp)
    elif assert_type=='jsonPath':
        return assertUtil.jsonPath_assert(json_path_str=assert_content,expecet_result=expect_result,obj=resp)
    elif assert_type=='sql':
        # try:
        assert_content=eval(assert_content)
        return assertUtil.sql_assert(dataBaseType=0,sql_statement=assert_content['sql_statement'],dataBaseConnectInfo=assert_content['dataBaseConnectInfo'],
                                 expect_result=expect_result,obj=resp,limitOne=True)
        # except Exception as e:
        #     traceback.print_stack()
    elif assert_type=='dict':
        return assertUtil.map_assert(a=expect_result,b=resp)
    else:
        print("断言类型不存在")
        return True
        # raise AssertionAnomaly(title="断言失败",content="断言类型不存在")



def run_all_cases(modeladmin, request, queryset):
    '''执行接口请求调试'''
    res = RunMethod()
    cases=case()
    case_list=case.objects.filter(case_is_run=1).order_by('id')
    # 执行前先将之前所有的测试用例用例标记更新为不是最新的
    caseLog.objects.filter(Q(caseLog_type='info') & Q(caseLog_last_run_lable=1)).update(caseLog_last_run_lable=0)
    case_report_start_time=datetime.datetime.now().replace(microsecond=0)
    for obj in case_list:
        cases = case()
        # cases.__dict__.update(obj.__dict__)
        # 注意这里需要使用模型来调用
        # case_obj_list=case.objects.filter(case_name=obj) #filter:返回一个queryset对象
        case_obj=case.objects.get(case_name=obj) #返回唯一对象，如果有多个对象，将触发异常 get() returned more than one case -- it returned n（n为对象数量）!
        # 获取用例关联的接口信息
        case_api_ids_obj=case_obj.case_api_ids
        api_domin_name=case_api_ids_obj.api_domain.domain_name
        apiUrl = api_domin_name + case_api_ids_obj.api_url
        api_method=case_api_ids_obj.api_req_method
        api_data=case_api_ids_obj.api_request_data
        api_header=case_api_ids_obj.api_header
        result = res.run_main(url=apiUrl,method=api_method,data=api_data,headers=api_header.header_data)
        case_run_status=assert_public(assert_type=case_obj.case_assert_type,assert_content=case_obj.case_assert_content,
                                      expect_result=case_obj.case_expect_result,resp=result)
        # print("case_run_status:",case_run_status)
        '''写入用例执行日志'''
        write_caseLog(reqeust=request,obj=case_obj,log_type='info',resp=result,res=res,case_is_pass=case_run_status)
    '''写入测试报告'''
    write_testCaseReport(request,case_report_start_time)
    # casse_report_id=caseReport.objects.order_by('id').values('id').first()
    casse_report_id=caseReport.objects.order_by('-id').values('id').first() #字段前加“-”代表降序，不加代表升序
    if not  casse_report_id:
        raise Exception("测试报告不存在")
    caseLog.objects.filter(caseLog_last_run_lable=1).update(caseLog_report_id=casse_report_id['id'])#将测试报告id写入caseLog
    messages.add_message(request, messages.INFO, '执行完毕')  # 在页面上展示的消息

class caseAdmin(commonAdmin):
    exclude = ()
    actions =[executeRequest,run_all_cases]

executeRequest.short_description = u'执行请求调试' #指定函数按钮名称
executeRequest.type = 'primary'  # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
run_all_cases.short_description = u'执行所有非跳过执行的用例' #指定函数按钮名称
run_all_cases.type = 'success'  # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button

class caseLogAdmin(readOnlyAdmin):
    # exclude = ('caseLog_resp',)
    def save_model(self, request, obj, form, change):
        '''admin内定义好的有特定含义的属性'''
        obj.creator = request.user  # 创建人为当前登录人
        super().save_model(request, obj, form, change)


class caseReportAdmin(commonAdmin):
    # list_display = ['show_report_route']

    def get_list_display(self, request):
        list_display_field=super().get_list_display(request)
        list_display_field.insert(0,"show_report_route")
        return list_display_field

    def show_report_route(self, obj):
        '''页面上展示测试报告'''
        #return format_html("<a href='url'>{url}</a><base target='_blank'/>", url=obj.report_route)
        # report_id = caseReport.objects.order_by('-id').values('id').first()
        # print(obj)
        return mark_safe(u'<a href="/report/%s" target="_blank">%s</a' % (obj.id, "查看报告"))


    show_report_route.short_description = "测试报告"
    # show_report_route.type = 'info'
    show_report_route.type = 'success'

admin.site.register(case, caseAdmin)
admin.site.register(caseLog, caseLogAdmin)
admin.site.register(caseReport, caseReportAdmin)

