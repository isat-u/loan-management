from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'middle_name', 'last_name', 'gender']
    search_fields = ['first_name', 'middle_name', 'last_name']
    list_filter = ['gender']


admin.site.register(User, UserAdmin)
