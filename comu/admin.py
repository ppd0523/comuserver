from django.contrib import admin

# Register your models here.
from .models import Filter, Report

admin.site.register(Filter)
admin.site.register(Report)
