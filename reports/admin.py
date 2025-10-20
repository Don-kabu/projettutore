from django.contrib import admin
from .models import Fuite

@admin.register(Fuite)
class FuiteAdmin(admin.ModelAdmin):
    list_display = ('complaint_name','phone','is_owner')