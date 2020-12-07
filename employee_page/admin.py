from django.contrib import admin
from employee_page.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(Employees)
admin.site.register(Departments)
admin.site.register(DeptEmp)
admin.site.register(DeptManager)
admin.site.register(Salaries)
admin.site.register(Titles)
