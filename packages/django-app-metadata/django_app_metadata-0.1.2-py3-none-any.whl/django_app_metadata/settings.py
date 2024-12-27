import django_environment_settings

# 是否启用缓存。默认：启用。
DJANGO_APP_METADATA_USE_CACHE = django_environment_settings.get(
    "DJANGO_APP_METADATA_USE_CACHE",
    True,
)
# 缓存时长。默认：1小时。
DJANGO_APP_METADATA_CACHE_TIMEOUT = django_environment_settings.get(
    "DJANGO_APP_METADATA_CACHE_TIMEOUT",
    60 * 60,
)
# 缺失配置项缓存时长。默认：5分钟。
DJANGO_APP_METADATA_MISSING_CONFIG_CACHE_TIMEOUT = django_environment_settings.get(
    "DJANGO_APP_METADATA_MISSING_CONFIG_CACHE_TIMEOUT",
    5 * 60,
)
# 缓存数据库名称。默认为：default。
DJANGO_APP_METADATA_CACHE_NAME = django_environment_settings.get(
    "DJANGO_APP_METADATA_CACHE_NAME",
    "default",
)
# 缓存项模板。默认为："django_app_metadata_cache:{key}"
DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE = django_environment_settings.get(
    "DJANGO_APP_METADATA_CACHE_KEY_TEMPLATE",
    "django_app_metadata_cache:{key}",
)
