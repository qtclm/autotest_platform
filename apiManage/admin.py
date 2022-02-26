from Common.modelAdmin_common import *
# Register your models here.
from apiManage.models import environment, domain, api, haeder


class environmentAdmin(commonAdmin):
    # list_display = []
    exclude = ()


class domainAdmin(commonAdmin):
    # list_display = []
    exclude = ()


class apiAdmin(commonAdmin):
    # list_display = []
    exclude = ()


class headerAdmin(commonAdmin):
    # list_display = []
    exclude = ()


admin.site.register(environment, environmentAdmin)
admin.site.register(domain, domainAdmin)
admin.site.register(api, apiAdmin)
admin.site.register(haeder, headerAdmin)
