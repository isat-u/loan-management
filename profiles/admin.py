from django.contrib import admin

# Register your models here.
from profiles.models import Profile
from profiles.models.profile_models import Gender


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'middle_name', 'last_name', 'gender']
    search_fields = ['first_name', 'middle_name', 'last_name']
    list_filter = ['gender']


admin.site.register(Profile, ProfileAdmin)


class GenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


admin.site.register(Gender, GenderAdmin)
