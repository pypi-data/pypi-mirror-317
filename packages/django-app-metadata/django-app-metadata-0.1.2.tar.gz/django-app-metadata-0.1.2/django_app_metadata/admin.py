from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_model_helper.admin import WithEnabledStatusFieldsAdmin
from django_model_helper.admin import WithDeletedStatusFieldsAdmin
from .models import Category
from .models import Config


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "display_order",
    ]
    search_fields = [
        "title",
    ]
    list_editable = [
        "display_order",
    ]
    readonly_fields = [
        "add_time",
        "mod_time",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "display_order",
                ],
            },
        )
    ]


class ConfigAdmin(
    ImportExportModelAdmin,
    WithEnabledStatusFieldsAdmin,
    WithDeletedStatusFieldsAdmin,
    admin.ModelAdmin,
):
    list_display = [
        "key",
        "description",
        "category",
        "published",
        "enabled",
        "deleted",
        "is_valid",
        "enabled",
    ]
    list_filter = [
        "is_valid",
        "published",
        "enabled",
        "deleted",
        "category",
    ]
    search_fields = [
        "key",
        "description",
        "data_raw",
    ]
    fieldsets = [
        (
            "基础信息",
            {
                "fields": [
                    "category",
                    "key",
                    "description",
                    "type",
                    "is_valid",
                    "data_raw",
                    "enabled",
                    "deleted",
                    "published",
                ]
            },
        ),
        (
            "其它信息",
            {
                "fields": [
                    "add_time",
                    "mod_time",
                    "enabled_time",
                    "disabled_time",
                    "published_time",
                    "unpublished_time",
                    "deleted_time",
                ]
            },
        ),
    ]
    readonly_fields = [
        "add_time",
        "mod_time",
        "enabled_time",
        "disabled_time",
        "published_time",
        "unpublished_time",
        "deleted_time",
        "is_valid",
    ]
    autocomplete_fields = [
        "category",
    ]


admin.site.register(Config, ConfigAdmin)
admin.site.register(Category, CategoryAdmin)
