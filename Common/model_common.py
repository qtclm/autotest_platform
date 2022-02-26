from django.db import models


class model_common_field(object):
    bool_enum = [
        (1, 'true'),
        (0, 'false'),
    ]


# 获取model信息，过滤id字段
def get_model_dict(obj: models.Model) -> dict:
    out_obj = obj.__dict__
    out_obj.pop('_state')
    out_obj.pop('id')
    return out_obj
