from django.apps import AppConfig


class DjangoAppConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_app_metadata"
    verbose_name = "数据字典管理"
