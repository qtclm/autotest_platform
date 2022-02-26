import django
from django.contrib.auth.models import User
from django.db import models
from caseManage.models import case

# Create your models here.

class gLobal_data(models.Model):

    global_data_key=models.CharField(verbose_name="全局数据key",max_length=256,blank=False)
    global_data_value=models.TextField(verbose_name="全局数据值",default="")
    global_data_desc=models.CharField(verbose_name="描述",default="",blank=True)
    global_data_case=models.ForeignKey(case,verbose_name="全局数据关联的用例，可为空",blank=True,on_delete=models.SET_NULL,editable=False)
    create_date=models.DateTimeField(verbose_name="创建时间",default=django.utils.timezone.now)
    create_user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,verbose_name="创建用户")


class public_function(models.Model):

    public_function_obj=models.JSONField(verbose_name="公共方法对象",help_text="包含函数对象名、参数")
    public_function_name=models.CharField(verbose_name="公共方法名称",max_length=128)
    public_function_desc=models.TextField(verbose_name="方法方法")
    create_date=models.DateTimeField(verbose_name="创建时间",default=django.utils.timezone.now)
    create_user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,verbose_name="创建用户")

