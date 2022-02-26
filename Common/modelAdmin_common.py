from django.contrib import admin

import  collections

# 只读model
class commonAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_list_display(self, request):
        return [self.short_detail(field.name) for field in self.model._meta.concrete_fields]

    # 控制显示长度，必须在adminx的list_display变量中改为函数名
    def short_detail(self,filed):
        if len(str(filed)) > 30:
            return '{}...'.format(str(filed)[0:29])
        else:
            return str(filed)

    short_detail.allow_tags = True
    short_detail.short_description = '响应信息'

    def register(self,obj):
        if collections.Iterable(obj):
            for i in obj:
                admin.site.register(i)
        else:
            admin.site.register(obj)




class readOnlyAdmin(commonAdmin):

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False