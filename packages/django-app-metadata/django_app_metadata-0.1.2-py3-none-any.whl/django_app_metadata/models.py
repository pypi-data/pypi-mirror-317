import logging
import yaml
import json
from zenutils import typingutils
from zenutils import jsonutils
from null_object import Null

from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.cache import caches

from django_safe_fields.fields import SafeTextField
from django_model_helper.models import WithAddModTimeFields
from django_model_helper.models import WithEnabledStatusFields
from django_model_helper.models import WithDeletedStatusFields
from django_model_helper.models import WithDisplayOrderFields
from django_model_helper.models import WithPublishStatusFields

from .exceptions import AccessToUnpublishedConfigIsForbidden
from .settings import DJANGO_APP_METADATA_USE_CACHE
from .settings import DJANGO_APP_METADATA_CACHE_TIMEOUT
from .settings import DJANGO_APP_METADATA_MISSING_CONFIG_CACHE_TIMEOUT
from .settings import DJANGO_APP_METADATA_CACHE_NAME
from .settings import DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE

_logger = logging.getLogger(__name__)


class Category(
    WithAddModTimeFields,
    WithDisplayOrderFields,
):
    title = models.CharField(
        max_length=64,
        verbose_name="名称",
    )

    class Meta:
        verbose_name = "配置项分类"
        verbose_name_plural = "配置项分类"

    def __str__(self):
        return self.title


class ConfigManager(models.Manager):
    pass


class ConfigQuerySet(models.QuerySet):
    def bulk_update(self, objs, fields, batch_size=None):
        # 对配置项执行bulk_update时需要删除所有key值对应的缓存
        cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
        for obj in objs:
            cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=obj.key)
            cache.delete(cache_key)
            _logger.debug(
                "config_bulk_update_delete_cache_key: id=%s, key=%s, cache_key=%s",
                obj.id,
                obj.key,
                cache_key,
            )
        # 如果key值也参与了批量更新
        # 需要查找出所有旧的key值并删除对应的缓存
        if "key" in fields:
            obj_ids = [obj.id for obj in objs]
            old_objs = Config.objects.filter(id__in=obj_ids)
            for obj in old_objs:
                cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=obj.key)
                cache.delete(cache_key)
                _logger.debug(
                    "config_bulk_update_delete_cache_key: id=%s, key=%s, cache_key=%s",
                    obj.id,
                    obj.key,
                    cache_key,
                )
        return super().bulk_update(objs, fields, batch_size)

    bulk_update.alters_data = True


class Config(
    WithAddModTimeFields,
    WithEnabledStatusFields,
    WithDeletedStatusFields,
    WithPublishStatusFields,
):
    objects = ConfigManager.from_queryset(ConfigQuerySet)()

    YAML = 10
    JSON = 20
    STRING = 30
    NUMBER = 40
    TYPE_CHOICES = [
        (YAML, "YAML格式"),
        (JSON, "JSON格式"),
        (STRING, "字符串"),
        (NUMBER, "数值型"),
    ]
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="分类",
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="配置项标识",
    )
    description = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="配置项说明",
    )
    type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=YAML,
        verbose_name="内容数据类型",
    )
    data_raw = SafeTextField(
        null=True,
        blank=True,
        verbose_name="配置项数据",
        help_text="如果设置的值与指定的类型不匹配，将视为NULL。",
    )
    is_valid = models.BooleanField(
        null=True,
        verbose_name="数据解析是否正确",
        editable=False,
        help_text="这里显示的是上一次保存时的数据解析结果。保存时会更新更新该字段。",
    )

    class Meta:
        verbose_name = "配置项"
        verbose_name_plural = "配置项"
        permissions = (
            [
                ("can_export_configs", "允许导出配置项"),
            ]
            + WithEnabledStatusFields.Meta.permissions
            + WithDeletedStatusFields.Meta.permissions
            + WithPublishStatusFields.Meta.permissions
        )

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.is_valid = self.validate()
        return super().save(*args, **kwargs)

    def get_type_code(self):
        return self.type

    def parse_data_raw(self):
        if not self.data_raw:
            return None
        if self.type == self.NUMBER:
            return typingutils.cast_numeric(self.data_raw)
        elif self.type == self.STRING:
            return self.data_raw
        elif self.type == self.JSON:
            return json.loads(self.data_raw)
        else:
            return yaml.safe_load(self.data_raw)

    def get_data(self):
        try:
            return self.parse_data_raw()
        except Exception as error:
            _logger.error(
                "字典数据解析失败：key=%s, data_raw=%s, error=%s",
                self.key,
                self.data_raw,
                error,
            )
            return None

    def set_data(self, data):
        if not data:
            self.data_raw = None
        if self.type == self.NUMBER:
            self.data_raw = data
        elif self.type == self.STRING:
            self.data_raw = data
        elif self.type == self.JSON:
            self.data_raw = jsonutils.simple_json_dumps(data, ensure_ascii=False)
        else:
            self.data_raw = yaml.safe_dump(data)
            self.type = self.YAML

    data = property(get_data, set_data)

    def info(self):
        return {
            "id": self.pk,
            "key": self.key,
            "data": self.data,
            "published": self.published,
        }

    def validate(self):
        try:
            data = self.parse_data_raw()
            return True
        except:
            return False

    @classmethod
    def get(
        cls,
        key,  # 配置项键名
        default=None,  # 如果数据库未设置该配置项时，该配置项的默认值。
        default_published=False,  # 如果数据库未设置该配置项时，该配置项的默认可访问性。
        use_cache=None,  # 是否使用缓存
        cache_timeout=None,  # 缓存超时时长
        missing_config_cache_timeout=None,
        frontend_flag=False,  # 是否前端查询
    ):
        if use_cache is None:
            use_cache = DJANGO_APP_METADATA_USE_CACHE
        if cache_timeout is None:
            cache_timeout = DJANGO_APP_METADATA_CACHE_TIMEOUT
        if missing_config_cache_timeout is None:
            missing_config_cache_timeout = (
                DJANGO_APP_METADATA_MISSING_CONFIG_CACHE_TIMEOUT
            )

        info = Null
        if (info is Null) and use_cache:
            if DJANGO_APP_METADATA_CACHE_NAME in caches:
                cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
                cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=key)
                info = cache.get(cache_key, Null)

        if info is Null:
            try:
                obj = cls.objects.get(key=key, enabled=True, deleted=False)
                info = obj.info()
            except cls.DoesNotExist:
                obj = None
                info = {
                    "id": 0,
                    "key": key,
                    "data": default,
                    "published": default_published,
                }
                cache_timeout = missing_config_cache_timeout
            if use_cache:
                if DJANGO_APP_METADATA_CACHE_NAME in caches:
                    cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
                    cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=key)
                    cache.set(cache_key, value=info, timeout=cache_timeout)

        if frontend_flag and (not info.get("published", False)):
            raise AccessToUnpublishedConfigIsForbidden()
        return info.get("data", default)


@receiver(signal=pre_save, sender=Config)
def config_pre_save_to_delete_cache_key(*args, **kwargs):
    # 保存前配置项前判断key值是否变化
    # 如果有变化，则删除旧key对应的缓存
    instance = kwargs.get("instance", None)
    if instance and instance.id:
        old_instance = Config.objects.get(id=instance.id)
        if old_instance.key != instance.key:
            cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
            cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(
                key=old_instance.key
            )
            cache.delete(cache_key)
            _logger.debug(
                "config_pre_save_to_delete_cache_key: id=%s, key=%s, cache_key=%s",
                instance.id,
                instance.key,
                cache_key,
            )


@receiver(signal=post_save, sender=Config)
def config_post_save_to_delete_cache_key(*args, **kwargs):
    # 保存配置项后删除key对应的缓存
    instance = kwargs.get("instance", None)
    if instance:
        cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
        cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=instance.key)
        cache.delete(cache_key)
        _logger.debug(
            "config_post_save_to_delete_cache_key: id=%s, key=%s, cache_key=%s",
            instance.id,
            instance.key,
            cache_key,
        )


@receiver(signal=post_delete, sender=Config)
def config_post_delete_to_delete_cache_key(*args, **kwargs):
    # 删除配置项后删除key对应的缓存
    instance = kwargs.get("instance", None)
    if instance:
        cache = caches[DJANGO_APP_METADATA_CACHE_NAME]
        cache_key = DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE.format(key=instance.key)
        cache.delete(cache_key)
        _logger.debug(
            "config_post_delete_to_delete_cache_key: id=%s, key=%s, cache_key=%s",
            instance.id,
            instance.key,
            cache_key,
        )
