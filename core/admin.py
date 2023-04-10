from django.contrib import admin

# Register your models here.
from .models import Company, Device


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("employees",)


class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "condition",
        "checked_out_by",
        "checked_out_datetime",
        "returned_datetime",
    )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Device, DeviceAdmin)
