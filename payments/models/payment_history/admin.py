from django.contrib import admin

from .models import PaymentHistory


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_date', 'payment_source', 'amount', 'status', 'account', 'loan', 'created']
    list_filter = ['id']
    search_fields = ['id']
    ordering = ['-created']

admin.site.register(PaymentHistory, PaymentHistoryAdmin)