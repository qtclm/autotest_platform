import traceback

from django.http import HttpResponse
# Create your views here.
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./caseManage/templates"))

from utils.generateReport import generateReport
import logging
from pyecharts import options as opts
from pyecharts.charts import Bar

# from caseManage.serializers import *
# from utils.response import APIResponse
from caseManage.models import *


def report(request):
    caseReportId = str(request.path_info)[8:]
    try:
        reportId = int(caseReportId)
        try:
            allReportData = caseReport.objects.get(id=reportId)
            reportLogData = caseLog.objects.filter(caseLog_report_id=reportId) #获取日志数据

            analyseTableList = [
                allReportData.caseReport_start_time, allReportData.caseReport_end_time, allReportData.caseReport_run_time,
                                int(allReportData.case_run_num),int(allReportData.case_pass_num),
                int(allReportData.case_fail_num),int(allReportData.case_skip_num)]  # 测试总结数据


            pieList = [ ['全部', allReportData.case_run_num],['通过', allReportData.case_pass_num],
                        ['失败', allReportData.case_fail_num], ['跳过', allReportData.case_skip_num]]
            # print(pieList)

            tableList = []

            for logData in reportLogData:
                case_info=case.objects.get(id=logData.caseLog_caseId)
                api_info=case_info.case_api_ids
                domain_info=api_info.api_domain
                version_info= api_info.api_version
                tableList.append([
                    domain_info.domain_project.project_name, version_info, domain_info.domain_environment,
                                  case_info.case_name, api_info.api_name, logData.caseLog_run_status,
                                  api_info.api_req_method, domain_info.domain_name+api_info.api_url, api_info.api_request_data,
                                  case_info.case_assert_type,case_info.case_assert_content, logData.caseLog_resp])
            # print(tableList)
            testReport = generateReport()
            page = testReport.make_pie_bar_info(analyseTableList, pieList, tableList)
            return HttpResponse(page.render_embed())

        except:
            logging.error('id=s% 的报告没找到，或是被删除了' % str(reportId))
            traceback.print_exc()
            # print("生成报告失败")
    except Exception as e:
        logging.error('获取的id不是数字，id=%s' % caseReportId)
        # traceback.print_exc()
        # print("获取测试报告信息失败")


def index(request):
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .add_yaxis("商家c", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return HttpResponse(c.render_embed())
