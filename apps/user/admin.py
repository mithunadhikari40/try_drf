from django.contrib import admin

from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll', 'city', 'by', 'created_at', 'updated_at']


admin.site.register(Student, StudentAdmin)
