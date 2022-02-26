#!/usr/bin/env/ python
# -*- coding: utf-8 -*-


class DatabaseError(Exception):
    def __init__(self, err='数据库连接异常,请查看本地MySql服务是否启动！', Reason=None):
        Exception.__init__(self, err, Reason)

class sqlExcuteError(Exception):
    def __init__(self, err='sql执行异常，请检查sql语法是否合法', Reason=None):
        Exception.__init__(self, err, Reason)

class ReadConfigError(Exception):
    def __init__(self, err='Config读取初始化失败', Reason=None):
        Exception.__init__(self, err, Reason)


class MailInitializationError(Exception):
    def __init__(self, err='邮件初始化', Reason=None):
        Exception.__init__(self, err, Reason)


class ReadYamlError(Exception):
    def __init__(self, err='Yaml读取初始化失败', Reason=None):
        Exception.__init__(self, err, Reason)


class AssertionAnomaly(Exception):
    def __init__(self, title=None, content=None):
        Exception.__init__(self, title, content)


class ReadExcelError(Exception):
    def __init__(self, err='读取Excel失败', Reason=None):
        Exception.__init__(self, err, Reason)


class CloseFileError(Exception):
    def __init__(self, err='关闭文件时发生错误', Reason=None):
        Exception.__init__(self, err, Reason)


class LogConfigError(Exception):
    def __init__(self, err='日志配置初始化错误', Reason=None):
        Exception.__init__(self, err, Reason)


class RequestError(Exception):
    def __init__(self, err='请求失败', Reason=None):
        Exception.__init__(self, err, Reason)


class StatusCodeAbnormal(Exception):
    def __init__(self, err='状态码异常', Reason=None):
        Exception.__init__(self, err, Reason)


class WriteResultError(Exception):
    def __init__(self, err='写入测试结果失败', Reason=None):
        Exception.__init__(self, err, Reason)



class ReadFileError(Exception):
    def __init__(self, err='读取文件失败', Reason=None):
        Exception.__init__(self, err, Reason)


class Ding_TalkError(Exception):
    def __init__(self, err='钉钉连接异常', Reason=None):
        Exception.__init__(self, err, Reason)


class JsonFormatError(Exception):
    def __init__(self, err='JSON格式化输出异常', Reason=None):
        Exception.__init__(self, err, Reason)


class ShellEnterError(Exception):
    def __init__(self, err='命令行输入异常'):
        Exception.__init__(self, err)


class GetTestCaseError(Exception):
    def __init__(self, err='获取测试用例异常'):
        Exception.__init__(self, err)

class dataTransformError(Exception):
    def __init__(self, err='数据转换异常',Reason=None):
        Exception.__init__(self, err,Reason)

class argsTypeError(Exception):
    def __init__(self, err='参数类型错误',Reason=None):
        Exception.__init__(self, err,Reason)

class jsonPathExtractError(Exception):
    def __init__(self, err='jsonpath提取失败',Reason=None):
        Exception.__init__(self, err,Reason)
