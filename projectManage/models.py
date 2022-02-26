import datetime

import django
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from Common.model_common import model_common_field


class project(models.Model):
    class Meta:
        verbose_name = _(u'项目列表')
        verbose_name_plural  = _(u'项目列表')
        db_table='project'

    project_name = models.CharField(max_length=32, blank=False, verbose_name='项目名称')
    project_desc = models.TextField(max_length=1024, blank=True, verbose_name='项目描述')
    project_state = models.BooleanField(default=True, choices=model_common_field.bool_enum, verbose_name='项目状态')
    # ForeignKey，外键关联，null:true允许为空，on_delete：被删除时设置字段为空 ,default:设置字段默认值
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now)

    # 外键关联时，默认展示str方法返回的对象值
    def __str__(self):
        return str(self.project_name)

# Create your models here.
class version(models.Model):

    class Meta:
        verbose_name = _(u'版本列表')
        # 设置此字段可避免app多展示一个s
        verbose_name_plural = _(u'版本列表')
        db_table='version'

    version_num = models.CharField(max_length=32, blank=False, verbose_name='版本号')
    version_name = models.CharField(max_length=128, blank=True, verbose_name='版本名称')
    version_desc = models.TextField(max_length=1024, blank=True, verbose_name='版本描述')
    version_state = models.BooleanField(default=True, choices=model_common_field.bool_enum, verbose_name='版本状态')
    # ForeignKey，外键关联，null:true允许为空，on_delete：被删除时设置字段为空
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL,default=User)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), default=django.utils.timezone.now)

    # 外键关联时，默认展示str方法返回的对象值
    def __str__(self):
        return str(self.version_name)+"_"+str(self.version_num)







