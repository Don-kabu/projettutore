from django.contrib import admin
from .models import Fuite

@admin.register(Fuite)
class FuiteAdmin(admin.ModelAdmin):
    list_display = ('description','latitude','longitude','date_signalement')