import uuid

from django.db import models
from django.db.models.fields.files import FieldFile

'''
基类，配合Dao使用
'''


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='标识')
    sort = models.IntegerField(null=True, unique=True, verbose_name='序号')
    name = models.CharField(max_length=255, null=True, verbose_name='名称')
    description = models.TextField(null=True, verbose_name='描述')
    date = models.DateField(null=True, verbose_name='日期')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')
    _enable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def mapping(self):
        mapping = {}
        for field in self._meta.get_fields():
            prop = field.name
            domain = type(field).__name__
            mapping[prop] = {'prop': prop, 'domain': domain, 'field': field}
        return mapping

    """
        只序列化基础字段：能用value_from_object直接取出的字段。与values等价
    """

    @property
    def json(self, fields={}):
        mapping = self.mapping
        excludes = ['ManyToOneRel', 'OneToOneRel', 'ManyToManyRel', 'ManyToManyField', 'UUIDField']
        mapping = {prop: mapping[prop] for prop in mapping if mapping[prop]['domain'] not in excludes}
        data = {}
        for prop in mapping:
            field = mapping[prop]['field']
            domain = mapping[prop]['domain']
            value = field.value_from_object(self)
            if domain in ['ForeignKey', 'OneToOneField']:
                prop = prop + '_id'
            elif domain in ['DateField']:
                value = value.strftime('%Y-%m-%d') if value else None
            elif domain in ['DateTimeField']:
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            elif domain in ['FileField']:
                file: FieldFile = value
                value = file.name
            # elif domain in ['BigAutoField']:
            #     value = str(value)
            data[prop] = value
        return data

    @property
    def full(self):
        data = self.json
        mapping = self.mapping
        excludes = ['ManyToManyField', 'ManyToManyRel', 'ForeignKey', 'ManyToOneRel', 'OneToOneField', 'OneToOneRel']
        mapping = {prop: mapping[prop] for prop in mapping if mapping[prop]['domain'] in excludes}
        for prop in mapping:
            field = mapping[prop]['field']
            domain = mapping[prop]['domain']
            if domain in ['ForeignKey', 'OneToOneField', 'OneToOneRel']:
                if hasattr(self, prop):
                    bean: BaseModel = getattr(self, prop)
                    data[prop] = bean.json if bean else None
            elif domain in ['ManyToManyField', 'ManyToManyRel', 'ManyToOneRel']:
                accessor = prop if domain == 'ManyToManyField' else field.get_accessor_name()
                try:
                    _set = getattr(self, accessor).all()
                    data[prop] = [item.id for item in _set]
                    data[f'{prop}_set'] = [item.json for item in _set]
                except Exception as e:
                    print(e)
                    pass
        return data


class BaseTree(BaseModel):
    pid = models.IntegerField(null=False, default=0, verbose_name='父节点')
    node_type = models.IntegerField(null=False, default=1, verbose_name='节点类型')  # 0 中间节点 1 末端节点
    icon = models.CharField(max_length=255, null=True, verbose_name='图标')

    class Meta:
        abstract = True
