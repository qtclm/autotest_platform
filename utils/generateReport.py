#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Tab, Page,Grid
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.options import ComponentTitleOpts
import time
import os


class generateReport():

    def make_pie_bar(self,pieNumList):
        '''生成测试结果的饼图和柱状图,且并行排序'''
        values = []
        for i in pieNumList:
            values.append(i[1])
        bar = (
            Bar()
            .add_xaxis(["测试结果"])
            .add_yaxis("全部", [values[0]])
            .add_yaxis("通过", [values[1]])
            .add_yaxis("失败", [values[2]])
            .add_yaxis("跳过", [values[3]])
            .set_colors(["green", "red", "orange","gray"])
            .set_global_opts(legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),)
        )

        pie = (
            Pie()
            .add("", pieNumList, center=["35%", "50%"],
                 radius=["40%", "75%"]
                 )
            .set_colors(["green", "red", "orange"])
            .set_global_opts(title_opts=opts.TitleOpts(title="测试用例运行结果"),
                             # legend_opts=opts.LegendOpts(pos_left="15%"),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
                             )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            # .render("pie_set_color1.html")
        )

        grid = (
            Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_left="60%"))
            .add(pie, grid_opts=opts.GridOpts(pos_top="50%", pos_right="75%"))
            #.render("./testReport/" + report_name + ".html")
        )
        return grid


    def make_case_able(self,tableList):
        '''本次测试运行的详细数据'''
        headers = [
            "测试项目", "所属版本", "测试环境",
                   "用例名称", "接口名称","是否通过", "请求方式", "请求接口", "请求参数", "断言类型",
                    "断言内容","返回结果"]
        table = (
            Table()
            .add(headers, tableList)
            .set_global_opts(title_opts=opts.TitleOpts(title="测试用例运行结果"))
            #table.render("table_base.html")
        )
        return table

    def make_analy_table(self,analyseTableList):
        '''概述'''
        analysetable = (
                Table()
                .add(["事件", '数据'],
                     [
                         ["开始时间",analyseTableList[0]],
                         ["结束时间",analyseTableList[1]],
                         ["测试用时","本次测试执行总用时"+str(analyseTableList[2]) + '秒'],
                         ["总用例数", "本次执行总用例数"+ "【" +str(analyseTableList[3]) + "】" + "个"],
                         ["通过用例", "本次执行成功用例"+"【"+ str(analyseTableList[4]) + "】" + "个"],
                         ["失败用例", "本次执行失败用例" + "【"+ str(analyseTableList[5]) + "】" + "个"],
                         ["跳过用例", "本次执行跳过用例数" + "【" + str(analyseTableList[6]) + "】" + "个"],
                     ]
                     )
                .set_global_opts(title_opts=ComponentTitleOpts(title="测试基本信息"))
                #.render("report_name" + ".html")
        )
        return analysetable

    def make_pie_bar_info(self,analyseTableList,pieNumList,tableList):
        '''概述+测试结果+详情'''
        report_name = "测试报告" + str(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
        page = (
            Page()
            .add(
                self.make_analy_table(analyseTableList),
                self.make_pie_bar(pieNumList),
                self.make_case_able(tableList),
            )
        )
        # page.render("./testReport/" + report_name + ".html")
        # reportRoute = os.path.abspath("./testReport/" + report_name + ".html")
        # return reportRoute
        return page




if __name__ == '__main__':
    greport = generateReport()
    # greport.pie_datazoom_slider([['通过',10],['失败',10],['跳过',20]])
    # rows = [
    #     ["1", 2, 3, 4,5,6,7,8,9,10,11],
    #     ["12", 12, 23, 34,45,56,67,78,89,"uin=1562587451&json=1&g_tk=1916754934	","https://qzone-music.qq.com//fcg-bin/cgi_playlist_xml.fcg	"],
    # ]
    # greport.make_case_able(rows)
    # greport.this_time_test_info([['通过',10],['失败',10],['跳过',20]],rows)

    greport.make_analy_table(list(range(6)))


