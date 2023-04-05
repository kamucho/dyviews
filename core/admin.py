from django.contrib import admin

from core.models import Function


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['name', 'params']
