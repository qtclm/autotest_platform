from Common.modelAdmin_common import *

# Register your models here.
from .models import project,version

# @admin.display(description='project')
# def upper_case_name(obj):
#     return ("%s %s" % (obj.creator, obj.project_name)).upper()


class projectAdmin(commonAdmin):
    # 定义列表不需要展示的字段
    exclude = ()
    # 使用 fields 选项在 “添加” 和 “更改” 页面的表单中进行简单的布局修改


class versionAdmin(commonAdmin):
    # list_display = []
    exclude = ()


admin.site.register(project,projectAdmin)
admin.site.register(version,versionAdmin)