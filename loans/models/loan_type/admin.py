from django.contrib import admin

from .models import LoanType


class LoanTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created']
    list_filter = ['id']
    search_fields = ['id']
    ordering = ['-created']

admin.site.register(LoanType, LoanTypeAdmin)